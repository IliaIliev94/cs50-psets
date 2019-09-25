#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Checks if the user has passed exactly two command line arguments (the file execution and the image)
    if (argc != 2)
    {
        fprintf(stderr, "Usage: recover image\n");
        return 1;
    }
    // Opens the image for reading
    FILE *fp = fopen(argv[1], "r");
    // Checks if the image has opened properly
    if (fp == NULL)
    {
        fprintf(stderr, "File cannot be opened\n");
        return 2;
    }
    // Declares the type and size of the buffer for temporarily storing the bytes of the file
    unsigned char buffer[512];
    //Declares a counter variable
    int j = 0;
    int flag = 0;
    char filename[7];
    FILE *img;
    // Iterates over the file 512 bytes at a time
    for (int i = 0; fread(buffer, 1, 512, fp) == 512; i++)
    {
        // Checks for the start of a new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If already found a JPEG close it
            if (j > 0)
            {
                fclose(img);
            }
            // Create the name for a new JPEG file
            sprintf(filename, "%03i.jpg", j);
            // Open it
            img = fopen(filename, "w");
            // Increment the counter by 1
            j++;
        }
        // If already found a JPEG, write to the file
        if (j > 0)
        {
            fwrite(buffer, 1, 512, img);
        }
    }
    fclose(img);
    fclose(fp);
    return 0;
}
