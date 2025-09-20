#include <stdio.h>
#include <signal.h>
#include <unistd.h>

// Custom handler for SIGINT (Ctrl+C)
void handle_sigint(int sig) {
    printf("\nCaught signal %d (Ctrl+C), but not quitting!\n", sig);
}

int main() {
    // Attach handler for SIGINT
    signal(SIGINT, handle_sigint);

    printf("Program running. Press Ctrl+C (it will be trapped).\n");
    printf("Press Ctrl+Z to stop or kill from another terminal.\n");

    while (1) {
        printf("Working...\n");
        sleep(2);
    }

    return 0;
}

