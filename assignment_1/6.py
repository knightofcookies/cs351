from typing import List, Set


def get_unique_elements(l: List) -> Set:
    return set(l)


arr = [1, 1, 3, 2, 3, 2, 3, 2, 2]
print(get_unique_elements(arr))
