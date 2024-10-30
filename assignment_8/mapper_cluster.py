#!/usr/bin/env python3
import sys
import math

# Define candidate points (sepal length and width only)
candidates = [
    (5.8, 4.0),
    (6.1, 2.8),
    (6.3, 2.7)
]

# Helper function to calculate Euclidean distance
def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Process each line from the dataset
for line in sys.stdin:
    parts = line.strip().split(",")
    sepal_length, sepal_width = float(parts[0]), float(parts[1])

    # Find the nearest candidate
    nearest_candidate = None
    min_distance = float("inf")
    for i, (cx, cy) in enumerate(candidates):
        distance = euclidean_distance(sepal_length, sepal_width, cx, cy)
        if distance < min_distance:
            min_distance = distance
            nearest_candidate = i

    # Output the nearest candidate index and the point's coordinates
    print(f"{nearest_candidate}\t{sepal_length},{sepal_width}")
