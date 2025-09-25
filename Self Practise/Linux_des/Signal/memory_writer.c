#include <stdio.h>      // For printf, perror
#include <stdlib.h>     // For exit
#include <sys/types.h>  // For key_t, shm functions
#include <sys/ipc.h>    // For IPC_CREAT, shmget, etc.
#include <sys/shm.h>    // For shared memory functions
#include <string.h>     // For strncpy

#define SHM_SIZE 1024   // Size of the shared memory segment (1 KB)

int main() {
    key_t key = 1234;  // Unique key to identify the shared memory segment
    int shmid;         // Shared memory segment ID
    char *data;        // Pointer to shared memory

    // 1. Create or access the shared memory segment with given key and size
    shmid = shmget(key, SHM_SIZE, 0644 | IPC_CREAT);
    if (shmid == -1) {           // If shmget fails, print error and exit
        perror("shmget");
        exit(1);
    }

    // 2. Attach the shared memory segment to our process's address space
    data = shmat(shmid, NULL, 0);
    if (data == (char *) -1) {   // If shmat fails, print error and exit
        perror("shmat");
        exit(1);
    }

    // 3. Write a string message to the shared memory
    const char *message = "Hello from your shared memory program!";
    strncpy(data, message, SHM_SIZE);  // Copy message safely to shared memory

    // 4. Print confirmation to the console
    printf("Message written to shared memory: \"%s\"\n", message);

    // 5. Detach the shared memory segment from the process's address space
    if (shmdt(data) == -1) {     // If detaching fails, print error and exit
        perror("shmdt");
        exit(1);
    }

    // 6. (Optional) We could remove the shared memory segment here if desired,
    //     but typically you'd let the reader remove it or use it multiple times.

    return 0;  // Successful exit
}
