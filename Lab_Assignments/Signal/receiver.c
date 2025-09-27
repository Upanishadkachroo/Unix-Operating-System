#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

// Signal handler
void handler(int sig) {
    if (sig == SIGUSR1)
        printf(" Received SIGUSR1 signal!\n");
    else if (sig == SIGUSR2)
        printf(" Received SIGUSR2 signal!\n");
}

int main() {
    printf("Receiver PID: %d\n", getpid());

    // Register handlers
    signal(SIGUSR1, handler);
    signal(SIGUSR2, handler);

    // Keep running and wait for signals
    while (1) {
        pause(); // wait for signal
    }

    return 0;
}
