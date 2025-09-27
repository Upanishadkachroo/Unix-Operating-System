#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/types.h>
#include <unistd.h>

#define SHM_SIZE 1024   // size of shared memory

int main() {
    key_t key;
    int shmid;
    char *data;
    int choice;

    // Generate unique key for shared memory
    key = ftok("shmfile", 65);   // "shmfile" can be any existing file

    // Create shared memory segment
    shmid = shmget(key, SHM_SIZE, 0666 | IPC_CREAT);
    if (shmid < 0) {
        perror("shmget");
        exit(1);
    }

    // Attach shared memory
    data = (char*) shmat(shmid, (void*)0, 0);
    if (data == (char*) -1) {
        perror("shmat");
        exit(1);
    }

    printf("1. Write to shared memory\n");
    printf("2. Read from shared memory\n");
    printf("Enter choice: ");
    scanf("%d", &choice);
    getchar(); // consume newline

    if (choice == 1) {
        printf("Enter a string to write: ");
        fgets(data, SHM_SIZE, stdin);
        printf("✅ Data written to shared memory.\n");
    }
    else if (choice == 2) {
        printf("📩 Data read from shared memory: %s\n", data);
    }
    else {
        printf("Invalid choice.\n");
    }

    // Detach shared memory
    shmdt(data);

    return 0;
}
