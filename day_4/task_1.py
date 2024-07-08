import os
import re
from dataclasses import dataclass


@dataclass
class ScratchCard:
    card_index: int
    winning_numbers: set[int]
    numbers_you_have: set[int]


class DataLoader:
    scratch_cards: list[ScratchCard]
    matches: list[set[int]]
    matches_count: list[int]

    def __init__(self):
        self.scratch_cards = self.load_card()
        self.matches = [
            self.compute_match(scratch_card) for scratch_card in self.scratch_cards
        ]
        self.matches_count = [len(match) for match in self.matches]
        self.matches_score = [
            2 ** (match_count - 1) if match_count > 0 else 0
            for match_count in self.matches_count
        ]
        self.total_score = sum(self.matches_score)

    def compute_match(self, scratch_card: ScratchCard) -> set[int]:
        matches = scratch_card.numbers_you_have.intersection(
            scratch_card.winning_numbers
        )
        return matches

    def extract_digits_from_str(self, raw_str: str) -> list[int]:
        string_split = re.sub(" +", " ", raw_str).strip().split(" ")
        return [int(x) for x in string_split]

    def read_line(self, raw_line: str) -> ScratchCard:
        colon_split = raw_line.split(":")
        card_index_str = colon_split[0]
        numbers_str = colon_split[1]
        pipe_split = numbers_str.split("|")
        winning_numbers = self.extract_digits_from_str(pipe_split[0])
        numbers_you_have = self.extract_digits_from_str(pipe_split[1])
        return ScratchCard(
            card_index=int(card_index_str.replace("Card ", "")),
            winning_numbers=set(winning_numbers),
            numbers_you_have=set(numbers_you_have),
        )

    def load_card(self) -> list[ScratchCard]:
        filepath = os.path.join(os.path.dirname(__file__), "data.txt")
        with open(filepath, "r") as file:
            raw_txt = file.read()

        line_split = raw_txt.split("\n")
        return [self.read_line(x) for x in line_split if x != ""]

    def __str__(self) -> str:
        res = ""
        for card, intersection, matches_score in zip(
            self.scratch_cards, self.matches, self.matches_score
        ):
            winning_str = ", ".join([str(x) for x in list(card.winning_numbers)])
            numbers_str = ", ".join([str(x) for x in list(card.numbers_you_have)])
            res += f"{card.card_index}\n"
            res += f"  Winning: {winning_str}\n"
            res += f"  Yours: {numbers_str}\n"
            res += f"  Matches: {intersection}"
            res += f"  Score: {matches_score:,.0f}"
            res += "\n"
        res += f"🎉Total Score: {self.total_score:,.0f}"
        return res


if __name__ == "__main__":
    scratch_cards = DataLoader()
    print(scratch_cards)
