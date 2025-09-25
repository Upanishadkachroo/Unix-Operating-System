#include<stdio.h>
#include<signal.h>
#include<unistd.h>

int sigcnt=0;

void signalhandler(int signum){
	printf("Signal recieved is %d\n", signum);
	sigcnt++;
	printf("Number of times signal recieved is %d\n", sigcnt);
}

int main(){
	signal(SIGINT, signalhandler);

	while(1){
		printf("hello users\n");
		printf("user process id %d\n", getpid());
		sleep(1);
	}

	
}

