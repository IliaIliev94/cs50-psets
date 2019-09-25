#include <stdio.h>
#include <cs50.h>
int main(void)
{
    //Promts the user for his name
    string name = get_string("What is your name?\n");
    //Prints hello and the name of the user
    printf("hello, %s\n", name);
}
