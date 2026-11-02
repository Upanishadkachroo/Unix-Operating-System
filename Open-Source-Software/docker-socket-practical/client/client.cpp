#include <iostream>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netdb.h>

using namespace std;

int main() {
    int sock;

    struct sockaddr_in serv_addr;

    char buffer[1024] = {0};

    // 1. Create TCP socket
    sock = socket(AF_INET, SOCK_STREAM, 0);

    if (sock < 0) {
        cerr << "Socket creation failed\n";
        return 1;
    }

    cout << "Client socket created successfully\n";

    // 2. Resolve Docker server hostname
    struct hostent *server = gethostbyname("server");

    if (server == nullptr) {
        cerr << "Could not resolve server hostname\n";
        close(sock);
        return 1;
    }

    // 3. Configure server address
    memset(&serv_addr, 0, sizeof(serv_addr));

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(5000);

    memcpy(&serv_addr.sin_addr.s_addr,
           server->h_addr_list[0],
           server->h_length);

    // 4. Connect to server
    if (connect(sock, (struct sockaddr *)&serv_addr,
                sizeof(serv_addr)) < 0) {
        cerr << "Connection failed\n";
        close(sock);
        return 1;
    }

    cout << "Connected to server successfully\n";

    // 5. Send message
    const char *message =
        "Hello Server! This message is from Docker Client.";

    send(sock, message, strlen(message), 0);

    cout << "Message sent to server\n";

    // 6. Receive server response
    int bytes_received = recv(sock, buffer,
                              sizeof(buffer) - 1, 0);

    if (bytes_received > 0) {
        buffer[bytes_received] = '\0';

        cout << "Response from server: "
             << buffer << endl;
    }

    // 7. Close socket
    close(sock);

    return 0;
}
