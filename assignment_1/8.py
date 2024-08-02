from typing import Dict


def squares_and_cubes_in_range(n: int) -> Dict:
    d = {}
    for i in range(0, n + 1):
        sq = i**2
        cb = sq * i
        d[i] = [sq, cb]
    return d


print(squares_and_cubes_in_range(3))
