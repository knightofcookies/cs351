from typing import List


def uppercase_words(word_list):
    return list(map(str.upper, word_list))


words = ["aa", "bb", "cd", "e"]
print(uppercase_words(words))
