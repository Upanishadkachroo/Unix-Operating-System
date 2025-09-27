#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

// Signal handler for SIGALRM
void handle_alarm(int sig) {
    printf("\n Time’s up! No input within 10 seconds.\n");
    exit(0);
}

int main() {
    char input[100];

    // Register signal handler
    signal(SIGALRM, handle_alarm);

    // Set alarm for 10 seconds
    alarm(10);

    printf("Enter some input within 10 seconds: "); 
    fflush(stdout);

    // Read user input
    if (fgets(input, sizeof(input), stdin) != NULL) {
        alarm(0); // Cancel alarm if input is given
        printf("You entered: %s\n", input);
    }

    return 0;
}
