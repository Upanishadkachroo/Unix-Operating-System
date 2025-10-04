#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>

void print_file_type(mode_t mode, char *name) {
    printf("%s : ", name);
    if (S_ISREG(mode)) printf("Regular File\n");
    else if (S_ISDIR(mode)) printf("Directory\n");
    else if (S_ISCHR(mode)) printf("Character Device\n");
    else if (S_ISBLK(mode)) printf("Block Device\n");
    else if (S_ISFIFO(mode)) printf("FIFO (Pipe)\n");
    else if (S_ISLNK(mode)) printf("Symbolic Link\n");
    else if (S_ISSOCK(mode)) printf("Socket\n");
    else printf("Unknown\n");
}

int main(int argc, char *argv[]) {
    struct stat fileStat;

    if (argc < 2) {
        printf("Usage: %s <file1> <file2> ...\n", argv[0]);
        return 1;
    }

    for (int i = 1; i < argc; i++) {
        if (lstat(argv[i], &fileStat) < 0) {
            perror("lstat");
            continue;
        }
        print_file_type(fileStat.st_mode, argv[i]);
    }

    return 0;
}

