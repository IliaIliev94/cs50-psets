from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    # Create a new list and remove the newlines from the two stings, essentialy converting them to lists
    matches = []
    a = a.split('\n')
    b = b.split('\n')

    # Iterate over a or b and check if it's lines are contained in b and are not contained in the matches list. If so append the lines to the matches list.
    for line in a:
        if line in b and line not in matches:
            matches.append(line)

    # Iterate over the whole matches list and replace the spaces with empty strings
    for line in matches:
        if line == " ":
            line = ""

    return matches


def sentences(a, b):
    """Return sentences in both a and b"""

    # Split a and b into sentances. Initialize an empty list to store the matching sentances.
    matches = []
    a = sent_tokenize(a)
    b = sent_tokenize(b)

    # Iterate over a and check if any of it's sentances are in b and are not in the matches list in order to avoid duplicates. If so then append the sentance to matches.
    for sentance in a:
        if sentance in b and sentance not in matches:
            matches.append(sentance)

    return matches


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    # Initialize an empty list to store the matching substrings.
    matches = []

    # Iterate over allthe substrings of length n in a and check if the substring is in b and not already in the matches list. If so then append the sbustring to matches.
    for i in range(n, len(a) + 1):
        temp = a[i - n:i]
        if temp in b and temp not in matches:
            matches.append(temp)

    return matches
