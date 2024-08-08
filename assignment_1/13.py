from typing import List


def uppercase_words(word_list) -> List:
    return list(map(str.upper, word_list)) # Using map to upper case words


words = ["aa", "bb", "cd", "e"]
print(uppercase_words(words))
