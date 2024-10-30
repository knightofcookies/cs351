#!/usr/bin/env python3
import sys
import string

# Read each line from standard input
for line in sys.stdin:
    # Remove punctuation and convert to lowercase
    line = line.translate(str.maketrans('', '', string.punctuation)).lower()
    # Split line into words
    words = line.strip().split()
    # Output each word with a count of 1
    for word in words:
        print(f"{word}\t1")
