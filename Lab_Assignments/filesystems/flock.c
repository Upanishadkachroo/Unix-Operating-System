#include <stdio.h>
#include <stdlib.h>
#include <sys/file.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>

int main() {
    char filename[256];
    int fd;
    struct stat st;

    printf("Enter file name: ");
    scanf("%s", filename);

    fd = open(filename, O_RDWR);
    if (fd < 0) {
        perror("open");
        exit(1);
    }

    if (fstat(fd, &st) < 0) {
        perror("fstat");
        close(fd);
        exit(1);
    }

    // Mandatory lock check: regular file + set-GID + group execute off
    if (S_ISREG(st.st_mode) && 
        (st.st_mode & S_ISGID) && 
        !(st.st_mode & S_IXGRP)) {
        printf("Mandatory locking is enabled on this file.\n");
    } else {
        printf("Only advisory locking is possible.\n");
    }

    printf("Trying to acquire exclusive lock...\n");
    if (flock(fd, LOCK_EX) < 0) {
        perror("flock");
        close(fd);
        exit(1);
    }

    printf("Lock acquired. Press Enter to release.\n");
    getchar(); // consume leftover newline
    getchar(); // wait for user

    flock(fd, LOCK_UN);
    printf("Lock released.\n");

    close(fd);
    return 0;
}

