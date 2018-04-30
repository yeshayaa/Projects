Written in version Python 3.6

The text_count.py file reads the 'infile' text file and counts each word. The 'infile' text is a partial review of Chapter IV from the book, "A Tale of Two Cities" authored by the classic English writer Charles Dickens.

Put both the text_count.py and two_cities.txt in the same new directory you create using the terminal. Note of the code, the  way text_count.py reads in the word count is to use a dict. The code then moves the words and count from a dict to a list.

Then ...

| To run the program for TEXT format as an output list in the command line,

-> python text_count.py two_cities.txt format=text

| To run the program for JSON format type in the command line,

-> python text_count.py two_cities.txt format=json

This will run your code. You should see the words and count.
