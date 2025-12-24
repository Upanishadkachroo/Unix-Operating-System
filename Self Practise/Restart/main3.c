#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<sys/wait.h>

int main(int argc, char* argv[]){
    int id=fork();

    if(id==0){
        sleep(1);
    }
    printf("current id:%d, parent id:%d\n", getpid(), getppid());
    
    if(id!=0){
        wait(NULL);
    }

    int res=wait(NULL);
    if(wait(NULL)==-1){
        printf("no children to wait for\n");
    }
    else{
        printf("%d finished execution\n", res);
    }
    
    return 0; 
}