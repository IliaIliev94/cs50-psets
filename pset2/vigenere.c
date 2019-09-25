#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
int shift(char c);
int main(int argc, string argv[])
{
    // Checks if the arguments are two, if not stop the program
    if (argc != 2)
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }
    // Assigns the length of the keyword to a variable for optimization purpouses, as it will be used multiple times
    int k = strlen(argv[1]);
    bool is_alpha = true;
    // A for loop to check if all the characters of the keyword are alphabetic
    for (int i = 0; i < k; i++)
    {
        if (!isalpha(argv[1][i]))
        {
            is_alpha = false;
        }
    }
    // If any of the keywords of the program aren't alphabetic, stop the program and return a message for correct use to the user
    if (is_alpha == false)
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }
    // Gets the plaintext from the user and stores it in a variable
    string plaintext = get_string("Plaintext: ");
    char key[strlen(plaintext)];
    char total[strlen(plaintext) + 1];
    int counter = 0;
    // Starts printing the ciphertext
    printf("Ciphertext: ");
    // Iterates over each character of the plaintext and adds the keyword to it, if the plaintext characters is alphabetic, else it just prints it
    for (int i = 0, j = strlen(plaintext); i < j; i++)
    {
        if (isalpha(plaintext[i]))
        {
            if (isupper(plaintext[i]))
            {
                key[i] = ((plaintext[i] - 'A') + (shift(argv[1][counter % k]))) % 26 + 'A';
            }
            else
            {
                key[i] = ((plaintext[i] - 'a') + (shift(argv[1][counter % k]))) % 26 + 'a';
            }
            counter++;
        }
        else
        {
            key[i] = plaintext[i];
        }
    }
    total[strlen(plaintext)] = '\0';
    // Prints a newline
    strcpy(total, key);
    printf("%s", total);
    printf("\n");

}
// Function to convert keyword character to number
int shift(char c)
{
    return toupper(c) - 'A';
}
