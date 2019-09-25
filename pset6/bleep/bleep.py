from cs50 import get_string
from sys import argv


def main():
    if len(argv) != 2:
        print("Usage: python bleep.py dictionary")
        exit(1)
    # Initialize an empty set
    bannedWords = set()
    # Open the file provided in the command line argument and read the words
    with open(argv[1]) as f:
        # Store the words in a set/list data structure and remove the newlines
        for line in f:
            bannedWords.add(line.strip("\n"))
    
    # Ask the user for the message
    msg = get_string("What message would you like to censor?\n")
    # Split the message
    msg = msg.split(" ")

    # Create a new list where the words that are in the banned text are replaced by '*'
    msg = [i.replace(i, hashes(len(i))) if i.lower() in bannedWords else i for i in msg] 
    
    # Convert the msg into a string and print the final message to the user    
    msg = " ".join(msg)
    print(msg)
                

# Funcion to replace 
def hashes(number):
    totalHashes = ""
    for i in range(number):
        totalHashes += "*"
    return totalHashes


if __name__ == "__main__":
    main()
