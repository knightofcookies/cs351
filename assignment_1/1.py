from typing import List

def str_to_list(string: str) -> List:
    return list(string)

s = "abc"
print(s, type(s))

l = str_to_list(s)
print(l, type(l))
