#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int number;
// Promts the user for a number between 1 and 8, until they input one
    do
    {
        number = get_int("Enter number between 1 and 8: ");
    }
    while (number < 1 || number > 8);
    // Creates the rows
    for (int i = 0; i < number; i++)
    {
        // Prints the spaces
        for (int j = number; j > i + 1; j--)
        {
            printf(" ");
        }
        //Prints the hashes
        for (int k = 0; k < i + 1; k++)
        {
            printf("#");
        }
        // Prints two spaces between the hashes
        for (int m = 0; m < 2; m++)
        {
            printf(" ");
        }
        // Prints the second hashes
        for (int k = 0; k < i + 1; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}
