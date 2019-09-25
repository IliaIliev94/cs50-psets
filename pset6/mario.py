from cs50 import get_int

# Main function which calls the get input function and prints the piramid


def main():

    height = get_user_input()

    # Prints the piramid on the basis of the number of rows the user has given as input in the height variable
    for i in range(height):
        for j in range(i + 1, height):
            print(" ", end="")
        for k in range(i + 1):
            print("#", end="")
        for l in range(2):
            print(" ", end="")
        for m in range(i + 1):
            print("#", end="")
        print()

# Promts the user for input until he gives a number between 1 and 8 and return that number


def get_user_input():
    while True:
        i = get_int("Height: ")
        if i >= 1 and i <= 8:
            return i


# Calls the main function
if __name__ == "__main__":
    main()