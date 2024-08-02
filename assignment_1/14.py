from typing import List
from functools import reduce


def find_product_of_array(l: List[int]) -> int:
    return reduce(lambda x, y: x * y, l)


print(find_product_of_array([1, 2, 3, 4, 5]))
