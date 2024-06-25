import pandas as pd
from load_data import Colors, GameData, load_game_data


def check_games(games: list[Colors]):
    colors = ["red", "blue", "green"]
    return {color: max([game[color] for game in games]) for color in colors}


if __name__ == "__main__":
    raw_data = load_game_data()
    results = []
    for game_set in raw_data:
        game_index = game_set["game_index"]
        games = game_set["games"]
        result = check_games(games)
        results.append({"game_index": game_index, **result})
    results_df = pd.DataFrame(results).assign(
        power=lambda x: x["red"] * x["green"] * x["blue"]
    )
    print(results_df.to_markdown())
    print(results_df.sum().to_markdown())
