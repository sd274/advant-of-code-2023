import pandas as pd
from load_data import Colors, GameData, load_game_data


def check_game(game: Colors):
    color_max = {"red": 12, "green": 13, "blue": 14}
    for color, max_cubes in color_max.items():
        if game[color] > max_cubes:
            return False
    return True


def check_games(games: list[Colors]):
    for game in games:
        game_result = check_game(game)
        if not game_result:
            return "impossible"
    return "possible"


if __name__ == "__main__":
    raw_data = load_game_data()
    results = []
    for game_set in raw_data:
        game_index = game_set["game_index"]
        games = game_set["games"]
        result = check_games(games)
        results.append({"game_index": game_index, "result": result})
    results_df = pd.DataFrame(results)
    print(results_df.to_markdown())
    possible_games = [x["game_index"] for x in results if x["result"] == "possible"]
    total = sum(possible_games)
    print(f"Total: {total:.0f}")
