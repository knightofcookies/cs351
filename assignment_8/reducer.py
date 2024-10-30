#!/usr/bin/env python3
import sys

current_word = None
current_count = 0

# Read each line from standard input
for line in sys.stdin:
    word, count = line.strip().split("\t")
    count = int(count)

    # If we're still on the same word, add to its count
    if word == current_word:
        current_count += count
    else:
        # Output the word and its count
        if current_word:
            print(f"{current_word}\t{current_count}")
        current_word = word
        current_count = count

# Output the final word's count
if current_word:
    print(f"{current_word}\t{current_count}")
