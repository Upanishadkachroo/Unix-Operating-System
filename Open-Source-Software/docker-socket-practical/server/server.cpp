#include <iostream>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

using namespace std;

int main() {
    int server_fd, client_fd;

    struct sockaddr_in address;

    char buffer[1024] = {0};

    // 1. Create TCP socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);

    if (server_fd < 0) {
        cerr << "Socket creation failed\n";
        return 1;
    }

    cout << "Server socket created successfully\n";

    // Allow quick reuse of the port
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR,
               &opt, sizeof(opt));

    // 2. Configure server address
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(5000);

    // 3. Bind socket to port 5000
    if (bind(server_fd, (struct sockaddr *)&address,
             sizeof(address)) < 0) {
        cerr << "Binding failed\n";
        close(server_fd);
        return 1;
    }

    cout << "Server bound to port 5000\n";

    // 4. Listen for connections
    if (listen(server_fd, 5) < 0) {
        cerr << "Listen failed\n";
        close(server_fd);
        return 1;
    }

    cout << "Server is listening for clients...\n";

    // 5. Accept client connection
    socklen_t addrlen = sizeof(address);

    client_fd = accept(server_fd,
                       (struct sockaddr *)&address,
                       &addrlen);

    if (client_fd < 0) {
        cerr << "Connection acceptance failed\n";
        close(server_fd);
        return 1;
    }

    cout << "Client connected successfully\n";

    // 6. Receive message
    int bytes_received = recv(client_fd, buffer,
                              sizeof(buffer) - 1, 0);

    if (bytes_received > 0) {
        buffer[bytes_received] = '\0';

        cout << "Message received from client: "
             << buffer << endl;

        // 7. Send acknowledgement
        const char *response =
            "Hello Client! Message received by server.";

        send(client_fd, response, strlen(response), 0);
    }

    // 8. Close sockets
    close(client_fd);
    close(server_fd);

    cout << "Server connection closed\n";

    return 0;
}
