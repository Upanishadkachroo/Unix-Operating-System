#include<stdio.h>

int main(){
    char cmd[100];

    while(1){
        printf("myshell> ");
        fgets(cmd, 100, stdin);

        printf("You typed: %s", cmd);
    }
}