#!/usr/bin/env python3
import sys

current_candidate = None
total_x = 0.0
total_y = 0.0
count = 0

# Read each line from standard input
for line in sys.stdin:
    candidate, coordinates = line.strip().split("\t")
    x, y = map(float, coordinates.split(","))

    if candidate == current_candidate:
        total_x += x
        total_y += y
        count += 1
    else:
        if current_candidate is not None:
            print(f"{current_candidate}\t{total_x / count},{total_y / count}")
        
        current_candidate = candidate
        total_x = x
        total_y = y
        count = 1

# Output the last candidate's new coordinates
if current_candidate is not None:
    print(f"{current_candidate}\t{total_x / count},{total_y / count}")
