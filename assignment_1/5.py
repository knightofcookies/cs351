from typing import List, Dict


def get_frequency_dict(l: List) -> Dict:
    frequencies = {}
    for element in l:
        if element in frequencies:
            frequencies[element] += 1
        else:
            frequencies[element] = 1
    return frequencies


arr = [1, 2, 3, 4, 5, 4, 3, 2, 1]
print(get_frequency_dict(arr))
