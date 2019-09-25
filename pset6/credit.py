from cs50 import get_int


def main():
    # Get the card number input from the user
    cardNumber = str(get_int("Number: "))
    # Call the card_validation function and recieve the summed number
    valid = card_validation(cardNumber)
    # Chekc if the number is a valid card number
    if valid % 10 == 0:
        # Check to which card company does the number correspond (AMEX, Visa or MasterCard), if it doesn't to any then print invalid
        if len(cardNumber) == 16 and cardNumber[0] == '5' and (cardNumber[1] == '1' or cardNumber[1] == '2' or cardNumber[1] == '3' or cardNumber[1] == '4' or cardNumber[1] == '5'):
            print("MASTERCARD")

        elif len(cardNumber) == 15 and cardNumber[0] == '3' and(cardNumber[1] == '4' or cardNumber[1] == '7'):
            print("AMEX")

        elif (len(cardNumber) == 13 or len(cardNumber) == 16) and cardNumber[0] == '4':
            print("VISA")

        else:
            print("INVALID")
    # If the card number isn't valid print "INVALID"
    else:
        print("INVALID")

# Function to sum the numbers of the credit card number according to Lugn's algorithm


def card_validation(cardNumber):
    # Intiliza the varable that will store the final number from the sumation
    totalSum = 0
    # Iterate over every other digit startin from the last one. Afetwards add the sum to the total sum.
    for i in range(len(cardNumber) - 1, -1, -2):
        totalSum += int(cardNumber[i])
    # Iterate over every other digit starting from the second last one and multiply it by two. If the product is two or more digits long sum the digits of the product. Afetwards add the sum to the total sum.
    for j in range(len(cardNumber) - 2, -1, -2):
        temp = str(int(cardNumber[j]) * 2)

        for i in range(len(temp)):
            totalSum += int(temp[i])

    return totalSum


# Call the main function
if __name__ == "__main__":
    main()