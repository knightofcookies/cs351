from typing import List
import random


def generate_n_random_numbers(n: int) -> List:
    return [random.randint(1, n) for _ in range(0, n)]


print(generate_n_random_numbers(5))
