from sys import argv
from cs50 import get_string

keyLength = len(argv[1])


def main():

    # Check if the user has inputted the right number of arguments
    if len(argv) != 2:
        print("Usage: python vigenere.py key")
        exit(1)

    # Chekcs if the key contains any non-alphabetic characters
    for i in range(keyLength):
        if not argv[1][i].isalpha():
            print("Input should consist only of alphabetic characters")
            exit(1)

    # Get the plainyext from the user and print it
    plaintext = get_string("Plaintext: ")

    print(f"ciphertext: {encrypt(plaintext, argv[1])}",)

# Function to encrypt the plaintext


def encrypt(plaintext, key):
    ciphertext = ""
    j = 0
    # Iterates over characters in plaintext
    for i in plaintext:
        # Checks if character from plaintext is alphabetic, and if so proceed
        if i.isalpha():
            # Calculates the alphabetic value for the corresponding character for the key. And also rotates the characters using array indexing.
            if key[j % keyLength].isupper():
                keyValue = ord(key[j % keyLength]) - 65

            else:
                keyValue = ord(key[j % keyLength]) - 97

            # Calculates the value for the ciphertext character
            if i.isupper():
                ciphertext += chr(((ord(i) - 65 + keyValue) % 26) + 65)

            else:
                ciphertext += chr(((ord(i) - 97 + keyValue) % 26) + 97)

            j += 1

        # If the plaintext character isn't alphabetic just copy it to the ciphertext
        else:
            ciphertext += i

    return ciphertext


if __name__ == "__main__":
    main()

