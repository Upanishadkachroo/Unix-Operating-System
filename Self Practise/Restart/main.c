#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>

int main(int argc, char* argv[]){
    // int id=fork();
    //printf("Hello World from id: %d\n", id);
    //0 process is child process
    // if(id==0){
    //     printf("Hello from the child process: %d\n", id);
    // }
    // else{
    //     printf("Hello from the parent process: %d\n", id);
    // }

    // fork();
    // fork();
    // printf("Hello\n");

    //to get three process
    int id1=fork();
    if(id1!=0){//parent process to create child
        fork();
    }
    printf("Hello\n");
    return 0;
}