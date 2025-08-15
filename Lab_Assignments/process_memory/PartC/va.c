// Program to print location of main and heap allocated value returned from malloc

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char * argv[]) {

    //main is the function pointer
    //main gives address of the code segement in your process virtual address
    printf("location of code : %p\n", main); 

    //heap starts above the global data segment and grows towards higher data add.
    //gives pointer to the virtual address
    printf("location of heap : %p\n", malloc(100e6));


    //The stack is located near the top of the process's address space and grows downward toward lower addresses.
    //Printing &x gives the virtual address of that stack slot.
    int x=3;

    printf("location of stack: %p\n", &x);




    //the output only shows the virtual address of the program 
    //To view the actual addresss use kernel APIs like /prrc/<PID>/pagemap
    return x;

}

