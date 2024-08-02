from typing import List


def create_list_of_tuples(l1: List, l2: List) -> List:
    return list(zip(l1, l2))


print(create_list_of_tuples([1, 2, 3, 4], ["a", "b", "c", "d"]))
