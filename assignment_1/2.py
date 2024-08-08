from typing import List


def str_to_list(string: str) -> List:
    return list(string)  # Iterable to list


def list_to_str(ls: List) -> str:
    return "".join(ls) # Using join()


s = "abc"  # Test string
print(s, type(s))  # "abc", str

l = str_to_list(s)
print(l, type(l))

s2 = list_to_str(l)
print(s2, type(s2))
