import re

from data import doc

number_str_map = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def get_index_of_match(word: str, matching_str: str, digit: str):
    word_index = None
    digit_index = None
    pattern = re.compile(matching_str)
    r = pattern.search(word)
    if r:
        word_index = r.start()
    digit_match = re.compile(digit).search(word)
    if digit_match:
        digit_index = digit_match.start()
    matching_indexs = [word_index, digit_index]
    matching_indexs_clean = [x for x in matching_indexs if x is not None]
    if len(matching_indexs_clean) == 0:
        return None
    return min(matching_indexs_clean)


def get_first_digit(word: str) -> str:
    index_map = {
        key: get_index_of_match(word, key, value)
        for key, value in number_str_map.items()
    }
    if all([x is None for x in index_map.values()]):
        return None
    index_map_clean = {
        key: value for key, value in index_map.items() if value is not None
    }
    min_key = min(index_map_clean, key=index_map_clean.get)
    return number_str_map[min_key]


def get_last_digit(word: str) -> str:
    index_map = {
        key: get_index_of_match(word[::-1], key[::-1], value)
        for key, value in number_str_map.items()
    }
    if all([x is None for x in index_map.values()]):
        return None
    index_map_clean = {
        key: value for key, value in index_map.items() if value is not None
    }
    min_key = min(index_map_clean, key=index_map_clean.get)
    return number_str_map[min_key]


def create_digit(word: str) -> int:
    first_digit = get_first_digit(word)
    last_digit = get_last_digit(word)
    digit = int(first_digit + last_digit)
    return digit


if __name__ == "__main__":
    total = 0
    for word in doc:
        total += create_digit(word)
    print(total)
