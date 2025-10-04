#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <unistd.h>
#include <string.h>

void print_file_type(mode_t mode) {
    if (S_ISREG(mode)) printf("File Type: Regular File\n");
    else if (S_ISDIR(mode)) printf("File Type: Directory\n");
    else if (S_ISCHR(mode)) printf("File Type: Character Device\n");
    else if (S_ISBLK(mode)) printf("File Type: Block Device\n");
    else if (S_ISFIFO(mode)) printf("File Type: FIFO (Pipe)\n");
    else if (S_ISLNK(mode)) printf("File Type: Symbolic Link\n");
    else if (S_ISSOCK(mode)) printf("File Type: Socket\n");
    else printf("File Type: Unknown\n");
}

int main() {
    char path[256];
    struct stat fileStat;

    printf("Enter file/directory path: ");
    scanf("%s", path);

    if (stat(path, &fileStat) < 0) {
        perror("stat");
        return 1;
    }

    printf("Inode Number: %ld\n", (long)fileStat.st_ino);
    printf("User ID: %d\n", fileStat.st_uid);
    printf("Group ID: %d\n", fileStat.st_gid);
    printf("File Access Permissions: %o\n", fileStat.st_mode & 0777);

    print_file_type(fileStat.st_mode);

    return 0;
}

