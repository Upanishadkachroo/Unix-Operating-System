#include <stdio.h>
#include <signal.h>
#include <unistd.h>

void signalhandler(int signum) {
    printf("Caught signal %d\n", signum);
}

int main() {
    pid_t pid = getpid();

    signal(SIGINT, signalhandler); 

    while (1) {
        kill(pid, SIGINT);  
        printf("User process id %d\n", pid);
        sleep(1);
    }

    return 0;
}
