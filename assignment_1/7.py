from typing import List


def first_repeating_element(l: List):
    unique_elements = set()
    for element in l:
        if element in unique_elements:
            return element
        unique_elements.add(element)


print(first_repeating_element([1, 2, 3, 4, 5, 1, 2]))
