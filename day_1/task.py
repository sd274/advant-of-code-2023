import re

from data import doc


def get_first_digit(word: str) -> str:
    for ch in word:
        if re.match("\d", ch):
            return ch


def get_last_digit(word: str) -> str:
    for ch in reversed(word):
        if re.match("\d", ch):
            return ch


def create_digit(word: str):
    first_digit = get_first_digit(word)
    last_digit = get_last_digit(word)
    digit_str = first_digit + last_digit
    return int(digit_str)


if __name__ == "__main__":
    total = 0
    for word in doc:
        total += create_digit(word)
    print(total)
