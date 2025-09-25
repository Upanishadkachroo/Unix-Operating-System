#include<signal.h>
#include<stdio.h>
#include<unistd.h>

void handler(int signum) {
    printf("Received signal %d\n", signum);
}


int main() {
    signal(SIGINT, handler);  // Register handler for Ctrl+C (SIGINT)

    while (1) {
        printf("Running...\n");
        sleep(1);
    }
    return 0;
}

