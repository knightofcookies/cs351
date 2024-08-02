from typing import List


def sort_in_descending_order(l: List[int]) -> List:
    l.sort(reverse=True)
    return l


arr = [1, 2, 3, 4, 5]
print(arr)
print(sort_in_descending_order(arr))
