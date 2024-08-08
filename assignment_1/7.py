from typing import List


def first_repeating_element(l: List):
    unique_elements = set()  # solution using a set
    for element in l:
        if element in unique_elements:  # if the element was seen before
            return element  # this is the first repeating element
        else:
            unique_elements.add(element)


print(first_repeating_element([1, 2, 3, 4, 5, 1, 2]))  # Output : 1
