import json
from typing import Tuple, TypedDict


def load_raw_str():
    with open("data.txt", "r") as f:
        raw_str = f.read()
    return raw_str


class Colors(TypedDict):
    red: int
    blue: int
    green: int


class GameData(TypedDict):
    game_index: int
    games: list[Colors]


def parse_single_color_str(color_str: str) -> Tuple[int, str]:
    colors = ["blue", "red", "green"]
    for color in colors:
        if color in color_str:
            return int(color_str.replace(color, "").strip()), color
    raise Exception("uh oh bad game")


def parse_game(raw_game: str) -> Colors:
    split_raw_game = raw_game.split(",")
    colors_parsed = [parse_single_color_str(x) for x in split_raw_game]
    color_dict = {"red": 0, "blue": 0, "green": 0}
    for color_count, parsed_color in colors_parsed:
        color_dict[parsed_color] += color_count
    return color_dict


def parse_line(line_str: str) -> GameData:
    game_str = line_str.split(":")[0].replace("Game ", "")
    try:
        game_index = int(game_str)
    except:
        print(line_str)
    games_raw = line_str.split(":")[1].split(";")
    games_paresed: list[Colors] = [parse_game(x) for x in games_raw]
    return {"game_index": game_index, "games": games_paresed}


def parse_raw_str(raw_str: str) -> list:
    raw_lines = raw_str.split("\n")
    raw_data = [parse_line(x) for x in raw_lines if x]
    return raw_data


def load_game_data():
    raw_data = load_raw_str()
    parsed_data = parse_raw_str(raw_data)
    return parsed_data


if __name__ == "__main__":
    data = load_game_data()
    print(json.dumps(data, indent=2))
