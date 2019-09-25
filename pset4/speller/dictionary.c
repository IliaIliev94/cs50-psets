// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <strings.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 65536

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];
// Traversal pointer
node *trav;
// Counter to keep track of loaded word into hashtable for the size function
unsigned int count = 0;

int number;
// Hashes word to a number between 0 and 65536, inclusive, based on bitwise operation on the characters of the string
unsigned int hash(const char *word)
{
    unsigned int hash = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        if (isupper(word[i]))
        {
            hash = (hash << 2) ^ (word[i] + ('a' - 'A'));
        }
        else
        {
            hash = (hash << 2) ^ word[i];
        }
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // Allocates a node
        trav = malloc(sizeof(node));
        // Checks if there is enough memory
        if (trav == NULL)
        {
            // If so unload the allocated memory and return false
            unload();
            return false;
        }
        //Create a new node and insert it into the hashtable
        number = hash(word);
        strcpy(trav -> word, word);
        trav -> next = hashtable[number];
        hashtable[number] = trav;
        //Increment the counter variable for the size function
        count++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // Return the counter for the total number of words loaded into the hashtable
    return count;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Assign the global trav pointer to the hashtable bucket of the string parameter
    trav = hashtable[hash(word)];
    // Iterate over every node and compare the string in each word with the string parameter
    while (trav != NULL)
    {
        if (strcasecmp(word, trav -> word) == 0)
        {
            return true;
        }
        trav = trav -> next;
    }
    // If the string wasn't found in the hashtable, return false
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // Initialize a temporary pointer
    node *temporary = NULL;
    // Iterate over the hasthable buckets and free each of their nodes
    for (int i = 0; i < N; i++)
    {
        trav = hashtable[i];
        while (trav != NULL)
        {
            temporary = trav;
            trav = trav -> next;
            free(temporary);

        }
    }
    return true;
}
