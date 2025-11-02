#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>

int main() {
    int fd = open("example.txt", O_RDONLY);  // Open file for reading

    if (fd == -1) {
        perror("open");
        return 1;
    }

    printf("File descriptor = %d\n", fd);  // Example: prints 3

    close(fd);  // Release the file descriptor
    return 0;
}

