#include <stdio.h>
#include <cs50.h>

int main(void)
{
    long number;
    int sum = 0;
    int i;
    int firstNumber;
    int secondNumber;
    number = get_long("Enter card number: ");
    // Gets the individual digit from the number
    for (i = 0; number != 0; number /= 10, i++)
    {
        // Checks for the second digit and stores it in a variable
        if (number > 9 && number < 100)
        {
            secondNumber = number % 10;
        }
        // Checks for the first digit and stores it in a variable
        if (number < 10)
        {
            firstNumber = number;
        }
        // Gets every digit starting from the last one and add it to the total sum
        if (i % 2 == 0)
        {
            sum += (number % 10);
        }
        // Gets every digit starting from the second to last one
        else
        {
            // Checks if the digit multiplied by two gives a number greater than 9, in other words if the digits are more than one
            if ((number % 10) * 2 > 9)
            {
                // If so just add the two digits together and add them to the total sum
                sum += ((number % 10) * 2) % 10 + (((number % 10) * 2) / 10) % 10;
            }
            // Else just multiply the digit by two and add it to the total sum
            else
            {
                sum += (number % 10) * 2;
            }

        }
    }
    // Chekc if the credit card is valid
    if (sum % 10 == 0)
    {
        // Checks if the credit card is Visa, American Express or Mastercard or other/invlaid
        if ((i == 13 || i == 16) && firstNumber == 4)
        {
            printf("VISA\n");
        }
        else if (i == 15 && (firstNumber == 3 && (secondNumber == 4 || secondNumber == 7)))
        {
            printf("AMEX\n");
        }
        else if (i == 16 && (firstNumber == 5 && (secondNumber == 1 || secondNumber == 2 || secondNumber == 3 || secondNumber == 4
                             || secondNumber == 5)))
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}
