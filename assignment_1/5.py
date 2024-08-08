from typing import List, Dict


def get_frequency_dict(l: List) -> Dict:
    frequencies = {}  # dictionary
    for element in l:
        if element in frequencies:  # if already seen
            frequencies[element] += 1
        else:  # first occurence
            frequencies[element] = 1
    return frequencies


arr = [1, 1, 3, 2, 3, 2, 3, 2, 2]
print(get_frequency_dict(arr))
