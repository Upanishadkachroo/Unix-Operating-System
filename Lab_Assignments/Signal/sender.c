#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

int main() {
    pid_t pid;
    int choice;

    printf("Enter PID of receiver process: ");
    scanf("%d", &pid);

    printf("Choose signal to send:\n");
    printf("1. SIGUSR1\n");
    printf("2. SIGUSR2\n");
    scanf("%d", &choice);

    if (choice == 1)
        kill(pid, SIGUSR1);
    else if (choice == 2)
        kill(pid, SIGUSR2);
    else
        printf("Invalid choice\n");

    return 0;
}
