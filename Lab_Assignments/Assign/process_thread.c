#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <pthread.h>

// Thread function
void* threadFunc(void* arg) {
    printf("Thread started: Thread ID = %lu\n", pthread_self());
    sleep(1);
    printf("Thread terminating: Thread ID = %lu\n", pthread_self());
    pthread_exit(NULL);
}

int main() {
    pid_t pid;
    pthread_t tid;

    printf("=== Process Creation and Termination ===\n");

    // Create process
    pid = fork();

    if (pid < 0) {
        perror("Fork failed");
        exit(1);
    }
    else if (pid == 0) { // Child process
        printf("Child process created. PID = %d\n", getpid());
        sleep(2);
        printf("Child process terminating. PID = %d\n", getpid());
        exit(0);
    }
    else { // Parent process
        printf("Parent process. PID = %d, Child PID = %d\n", getpid(), pid);
        wait(NULL); // Wait for child termination
        printf("Child terminated. Parent continues.\n");
    }

    printf("\n=== Thread Creation and Termination ===\n");

    // Create thread
    if (pthread_create(&tid, NULL, threadFunc, NULL) != 0) {
        perror("Thread creation failed");
        exit(1);
    }

    // Wait for thread to finish
    if (pthread_join(tid, NULL) != 0) {
        perror("Thread join failed");
        exit(1);
    }

    printf("Main thread exiting.\n");
    return 0;
}

