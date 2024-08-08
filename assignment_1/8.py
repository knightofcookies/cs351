from typing import Dict


def squares_and_cubes_in_range(n: int) -> Dict:
    d = {} # dictionary
    for i in range(0, n + 1):
        sq = i**2 # square
        cb = sq * i # cube
        d[i] = [sq, cb] # [square, cube]
    return d


print(squares_and_cubes_in_range(3))
