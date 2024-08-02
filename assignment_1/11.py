from typing import Dict


def generate_squares_upto_n(n: int) -> Dict:
    return {i:i**2 for i in range(0, n + 1)}


print(generate_squares_upto_n(5))
