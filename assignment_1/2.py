from typing import List

def list_to_str(ls: List) -> str:
    return str(ls)

l = ['a', 'b', 'c']
print(l, type(l))

s = list_to_str(l)
print(s, type(s))
