from typing import List


def str_to_list(string: str) -> List:
    return list(string)  # Iterable to list


s = "abc"  # Test string
print(s, type(s))  # "abc", str

l = str_to_list(s)
print(l, type(l))
