For this practical, we will create two separate C++ **TCP** socket applications, package each application into its own Docker image, push both images to Docker Hub, and run the containers on the same Docker network to demonstrate communication.

We will implement:

## Container 1 – TCP Server: Listens on port `5000` and receives messages.

## Container 2 – TCP Client: Connects to the server and sends a message.

The client will connect using the Docker container's service name, not `localhost`. This demonstrates Docker's container-to-container networking.

# Experiment: Socket communication between two Docker containers

## 1. Create the project structure

Open your Ubuntu terminal:

``` mkdir -p ~/docker-socket-practical/server mkdir -p ~/docker-socket-practical/client

cd ~/docker-socket-practical ```

The directory structure will be:

``` docker-socket-practical/ │ ├── server/ │   ├── server.cpp │   └── Dockerfile │ ├── client/ │   ├── client.cpp │   └── Dockerfile │ └── compose.yaml ```

## 2. Create the TCP server application

The server will:

- Create a **TCP** socket.
- Bind it to port `**5000**`.
- Listen for incoming connections.
- Accept a client connection.
- Receive and display the client's message.
- Send an acknowledgement back.

Create the file:

``` nano server/server.cpp ```

Paste this C++ code:

``` #include <iostream> #include <cstring> #include <unistd.h> #include <arpa/inet.h> #include <sys/socket.h>

using namespace std;

int main() {
    int server_fd, client_fd;

    struct sockaddr_in address;

    char buffer[**1024**] = {0};

    // 1. Create **TCP** socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);

    if (server_fd < 0) {
    cerr << *Socket creation failed\n*;
    return 1;
    }

    cout << *Server socket created successfully\n*;

    // Allow quick reuse of the port
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR,
    &opt, sizeof(opt));

    // 2. Configure server address
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(**5000**);

    // 3. Bind socket to port **5000**
    if (bind(server_fd, (struct sockaddr *)&address,
    sizeof(address)) < 0) {
    cerr << *Binding failed\n*;
    close(server_fd);
    return 1;
    }

    cout << *Server bound to port **5000**\n*;

    // 4. Listen for connections
    if (listen(server_fd, 5) < 0) {
    cerr << *Listen failed\n*;
    close(server_fd);
    return 1;
    }

    cout << *Server is listening for clients...\n*;

    // 5. Accept client connection
    socklen_t addrlen = sizeof(address);

    client_fd = accept(server_fd,
    (struct sockaddr *)&address,
    &addrlen);

    if (client_fd < 0) {
    cerr << *Connection acceptance failed\n*;
    close(server_fd);
    return 1;
    }

    cout << *Client connected successfully\n*;

    // 6. Receive message
    int bytes_received = recv(client_fd, buffer,
    sizeof(buffer) - 1, 0);

    if (bytes_received > 0) {
    buffer[bytes_received] = '\0';

    cout << *Message received from client: *
    << buffer << endl;

    // 7. Send acknowledgement
    const char *response =
    *Hello Client! Message received by server.*;

    send(client_fd, response, strlen(response), 0);
    }

    // 8. Close sockets
    close(client_fd);
    close(server_fd);

    cout << *Server connection closed\n*;

    return 0;
}
```

Save using `Ctrl + O`, Enter, and `Ctrl + X`.

### Understand the important socket functions

| Function   | Purpose                                      |
| ---------- | -------------------------------------------- |
| `socket()` | Creates a TCP socket                         |
| `bind()`   | Assigns an IP address and port to the server |
| `listen()` | Waits for incoming connections               |
| `accept()` | Accepts a client connection                  |
| `recv()`   | Receives data from the client                |
| `send()`   | Sends data to the client                     |
| `close()`  | Closes the socket                            |

`AF_INET` specifies IPv4, while `SOCK_STREAM` specifies **TCP**.

## 3. Create the server Dockerfile

``` nano server/Dockerfile ```

Paste:

``` **FROM** ubuntu:24.04

**RUN** apt-get update && \
    apt-get install -y g++ && \
    rm -rf /var/lib/apt/lists/*

**WORKDIR** /app

**COPY** server.cpp .

**RUN** g++ server.cpp -o server

**EXPOSE** **5000**

**CMD** [*./server*] ```

This Dockerfile:

- Downloads the Ubuntu base image.
- Installs the C++ compiler.
- Copies the server source code.
- Compiles the application.
- Exposes port `**5000**`.
- Starts the server when the container runs.

## 4. Create the TCP client application

The client will:

- Create a **TCP** socket.
- Resolve the server using its Docker network name.
- Connect to port `**5000**`.
- Send a message.
- Receive the server's acknowledgement.

Create the file:

``` nano client/client.cpp ```

Paste:

``` #include <iostream> #include <cstring> #include <unistd.h> #include <arpa/inet.h> #include <sys/socket.h> #include <netdb.h>

using namespace std;

int main() {
    int sock;

    struct sockaddr_in serv_addr;

    char buffer[**1024**] = {0};

    // 1. Create **TCP** socket
    sock = socket(AF_INET, SOCK_STREAM, 0);

    if (sock < 0) {
    cerr << *Socket creation failed\n*;
    return 1;
    }

    cout << *Client socket created successfully\n*;

    // 2. Resolve Docker server hostname
    struct hostent *server = gethostbyname(*server*);

    if (server == nullptr) {
    cerr << *Could not resolve server hostname\n*;
    close(sock);
    return 1;
    }

    // 3. Configure server address
    memset(&serv_addr, 0, sizeof(serv_addr));

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(**5000**);

    memcpy(&serv_addr.sin_addr.s_addr,
    server->h_addr_list[0],
    server->h_length);

    // 4. Connect to server
    if (connect(sock, (struct sockaddr *)&serv_addr,
    sizeof(serv_addr)) < 0) {
    cerr << *Connection failed\n*;
    close(sock);
    return 1;
    }

    cout << *Connected to server successfully\n*;

    // 5. Send message
    const char *message =
    *Hello Server! This message is from Docker Client.*;

    send(sock, message, strlen(message), 0);

    cout << *Message sent to server\n*;

    // 6. Receive server response
    int bytes_received = recv(sock, buffer,
    sizeof(buffer) - 1, 0);

    if (bytes_received > 0) {
    buffer[bytes_received] = '\0';

    cout << *Response from server: *
    << buffer << endl;
    }

    // 7. Close socket
    close(sock);

    return 0;
}
```

Save and exit.

Important: The hostname `server` is intentional. Docker Compose provides **DNS**-based service discovery, so the client can find the server container using this name.

## 5. Create the client Dockerfile

``` nano client/Dockerfile ```

Paste:

``` **FROM** ubuntu:24.04

**RUN** apt-get update && \
    apt-get install -y g++ && \
    rm -rf /var/lib/apt/lists/*

**WORKDIR** /app

**COPY** client.cpp .

**RUN** g++ client.cpp -o client

**CMD** [*./client*] ```

The client does not need `**EXPOSE**` because it initiates an outgoing connection rather than listening for incoming connections.

## 6. Create Docker Compose configuration

We will use Docker Compose to create a shared network and manage the two containers.

``` nano compose.yaml ```

Paste:

``` services:

    server:
    build: ./server
    image: YOUR_DOCKERHUB_USERNAME/socket-server:v1
    container_name: socket-server
    ports:
    - ***5000**:**5000***
    networks:
    - socket-network

    client:
    build: ./client
    image: YOUR_DOCKERHUB_USERNAME/socket-client:v1
    container_name: socket-client
    depends_on:
    - server
    networks:
    - socket-network

networks:
    socket-network:
    driver: bridge
```

Replace `YOUR_DOCKERHUB_USERNAME` with your actual Docker Hub username in both image names.

For example, if your Docker Hub username is `upanishad`, use:

``` image: upanishad/socket-server:v1 ```

and:

``` image: upanishad/socket-client:v1 ```

## 7. Build both Docker images

From the project root:

``` cd ~/docker-socket-practical ```

Build:

``` sudo docker compose build ```

Check the images:

``` sudo docker images ```

You should see two images:

| Image                                      | Purpose    |
| ------------------------------------------ | ---------- |
| `YOUR_DOCKERHUB_USERNAME/socket-server:v1` | TCP server |
| `YOUR_DOCKERHUB_USERNAME/socket-client:v1` | TCP client |

## 8. Run the server container

Start only the server:

``` sudo docker compose up -d server ```

Check:

``` sudo docker compose ps ```

View the server logs:

``` sudo docker logs socket-server ```

Expected output:

``` Server socket created successfully Server bound to port **5000** Server is listening for clients... ```

The server is now waiting for a client.

## 9. Run the client container

In the same terminal, execute:

``` sudo docker compose run --rm client ```

Expected client output:

``` Client socket created successfully Connected to server successfully Message sent to server Response from server: Hello Client! Message received by server. ```

Now check the server logs:

``` sudo docker logs socket-server ```

Expected server output:

``` Server socket created successfully Server bound to port **5000** Server is listening for clients... Client connected successfully Message received from client: Hello Server! This message is from Docker Client. Server connection closed ```

Communication demonstrated

The two applications have communicated through **TCP** sockets while running in separate Docker containers.

## 10. Understand how communication works

## Docker TCP communication

Client container

C++ **TCP** Client

Outgoing connection

**TCP** connection

server:**5000**

Server container

C++ **TCP** Server — port **5000**

Listening

Both containers are connected to the same Docker bridge network: socket-network.

The communication sequence is:

## The server creates a socket and binds it to port `5000`.

## The server starts listening. ## The client resolves the hostname `server` through Docker's internal DNS. ## The client connects to `server:5000`. ## The client sends a message. ## The server receives the message and sends an acknowledgement. ## The client receives the acknowledgement and closes the connection.

Why not use `localhost`?

Inside a Docker container, `localhost` refers to that same container. The client therefore cannot use `localhost:**5000**` to reach the server. It uses `server:**5000**` because both containers share the Compose network.

## 11. Push both images to Docker Hub

First, log in:

``` sudo docker login ```

Enter your Docker Hub credentials when prompted.

Push the server image:

``` sudo docker push YOUR_DOCKERHUB_USERNAME/socket-server:v1 ```

Push the client image:

``` sudo docker push YOUR_DOCKERHUB_USERNAME/socket-client:v1 ```

You should create two public repositories on Docker Hub:

- `socket-server`
- `socket-client`

Both images should appear in your Docker Hub account.

## 12. Pull the images and run them again

To demonstrate that the pushed images can be used independently of your local builds, first stop the Compose deployment:

``` sudo docker compose down ```

Remove the two locally built images:

``` sudo docker image rm YOUR_DOCKERHUB_USERNAME/socket-server:v1 sudo docker image rm YOUR_DOCKERHUB_USERNAME/socket-client:v1 ```

Pull them from Docker Hub:

``` sudo docker pull YOUR_DOCKERHUB_USERNAME/socket-server:v1 sudo docker pull YOUR_DOCKERHUB_USERNAME/socket-client:v1 ```

Now start the server using the pulled image:

``` sudo docker compose up -d server ```

Run the client using the pulled image:

``` sudo docker compose run --rm client ```

The same communication should occur.

Important: The `compose.yaml` image names must contain your actual Docker Hub username. Compose will use the pulled images rather than building them when you run these commands without `--build`.

## 13. Useful verification commands

| Command                                                              | Purpose                                              |
| -------------------------------------------------------------------- | ---------------------------------------------------- |
| `sudo docker ps`                                                     | Lists running containers                             |
| `sudo docker images`                                                 | Lists downloaded and built images                    |
| `sudo docker network ls`                                             | Lists Docker networks                                |
| `sudo docker network inspect docker-socket-practical_socket-network` | Inspects the Compose network                         |
| `sudo docker logs socket-server`                                     | Displays server-side communication                   |
| `sudo docker compose down`                                           | Stops and removes the containers and Compose network |

To inspect the network and confirm that both containers belong to it:

``` sudo docker network inspect docker-socket-practical_socket-network ```

The network name may vary if Compose uses a different project directory name.

## 14. Viva preparation

Q1. What is a socket?

A socket is an endpoint used for communication between two processes over a network. It is identified by an IP address and port number.

Q2. What is **TCP**?

**TCP** (Transmission Control Protocol) is a connection-oriented transport-layer protocol that provides reliable, ordered data delivery.

Q3. What is the difference between **TCP** and **UDP**?

| TCP                                      | UDP                        |
| ---------------------------------------- | -------------------------- |
| Connection-oriented                      | Connectionless             |
| Reliable delivery                        | No delivery guarantee      |
| Maintains data order                     | No inherent ordering       |
| Uses acknowledgements and retransmission | No built-in retransmission |
| More protocol overhead                   | Lower protocol overhead    |

Q4. What is the purpose of `bind()`?

It associates a server socket with a local IP address and port number.

Q5. What is the purpose of `listen()`?

It places the server socket into a passive listening state so it can accept incoming connection requests.

Q6. What is the purpose of `accept()`?

It accepts an incoming connection and returns a new socket descriptor for communication with that client.

Q7. Why do we use Docker networking?

Docker networking allows containers to communicate with one another using network addresses and **DNS**-based service names.

Q8. Why is the hostname `server` used in the client code?

Because Docker Compose registers service names in its internal **DNS**. The client can resolve `server` to the server container's IP address.

Q9. Why do we expose port **5000**?

Port `**5000**` is where the server listens. The Dockerfile's `**EXPOSE**` documents the intended port, while the Compose mapping `**5000**:**5000**` publishes it on the host.

**Q10**. Are two separate Docker images necessary?

They are not technically necessary, but we create two separate images here to demonstrate packaging and deploying independent client and server applications.

## 15. Experiment result

The experiment demonstrates **TCP** socket communication between two independent Docker containers. A C++ **TCP** server was deployed in one container, and a C++ **TCP** client was deployed in another. Both containers were connected through a Docker bridge network. The client successfully sent a message to the server, and the server returned an acknowledgement. Both Docker images were pushed to Docker Hub and subsequently pulled and executed.

Let's execute this in stages rather than troubleshooting the entire setup at once. Start with Steps 1–5 and share the output of:

``` cd ~/docker-socket-practical find . -maxdepth 2 -type f ```

I can verify that both applications and Dockerfiles are in the correct locations before we build the images.
