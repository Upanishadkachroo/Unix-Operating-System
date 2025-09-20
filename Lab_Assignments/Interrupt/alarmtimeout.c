#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

// Handler for SIGALRM
void handle_alarm(int sig) {
    printf("\nTime up! No input received within 10 seconds.\n");
    exit(1);  // terminate program
}

int main() {
    char input[100];

    // Register handler for SIGALRM
    signal(SIGALRM, handle_alarm);

    // Set alarm for 10 seconds
    alarm(10);

    printf("Enter something within 10 seconds: ");
    if (fgets(input, sizeof(input), stdin) != NULL) {
        // Cancel alarm if input received in time
        alarm(0);
        printf("You entered: %s\n", input);
    }

    return 0;
}

