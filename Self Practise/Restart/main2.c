#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>

int main(int argc, char* argv[]){
    int id=fork();
    if(id==0){
        sleep(1);
    }
    printf("Current id: %d, parent id: %df\n", getpid(), getppid());
    // if(id!=0){
    //     wait(NULL);
    // }

    int res=wait(NULL);
    if(res==-1){
        printf("No children to wait for\n"); 
    }else{
        printf("%d finished execution\n", res);
    }
    return 0;
}