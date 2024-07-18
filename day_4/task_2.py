import os
import re
from dataclasses import dataclass
from typing import Generator, Iterable


class ScratchCard:
    card_index: int
    winning_numbers: set[int]
    numbers_you_have: set[int]
    bonus_scratch_cards_lower: int
    bonus_scratch_card_upper: int

    def __init__(
        self, card_index: int, winning_numbers: set[int], numbers_you_have: set[int]
    ):
        self.card_index = card_index
        self.winning_numbers = winning_numbers
        self.numbers_you_have = numbers_you_have
        self.bonus_scratch_cards_lower, self.bonus_scratch_card_upper = (
            self.scratch_cards_to_add_to_children()
        )

    def compute_matches(self) -> set[int]:
        matches = self.numbers_you_have.intersection(self.winning_numbers)
        return matches

    def number_of_matches(self) -> int:
        matches = self.compute_matches()
        return len(matches)

    def scratch_cards_to_add_to_children(self) -> tuple[int, int]:
        lower = self.card_index + 1
        upper = lower + self.number_of_matches()
        return lower, upper


class ScratchCardWithChildren:
    scratch_card: ScratchCard
    children: list["ScratchCardWithChildren"]

    def __init__(
        self, scratch_card: ScratchCard, children: list["ScratchCardWithChildren"]
    ):
        self.scratch_card = scratch_card
        self.children = children

    def count_children(self) -> int:
        children_flat = list(self._flatten_children())
        return len(children_flat)

    def _flatten_children(self) -> Iterable["ScratchCardWithChildren"]:
        yield self
        for child in self.children:
            yield from child._flatten_children()


class DataLoader:
    original_scratch_cards: list[ScratchCard]

    def __init__(self):
        self.original_scratch_cards = self.load_card()
        self.scratch_cards_with_children = [
            self.create_scratch_card_with_children(scratch_card)
            for scratch_card in self.original_scratch_cards
        ]
        self.child_counts = [
            scratch_card_with_child.count_children()
            for scratch_card_with_child in self.scratch_cards_with_children
        ]

    def create_scratch_card_with_children(
        self, scratch_card: ScratchCard
    ) -> ScratchCardWithChildren:
        return ScratchCardWithChildren(
            scratch_card=scratch_card,
            children=[
                self.create_scratch_card_with_children(new_scratch_card)
                for new_scratch_card in self.original_scratch_cards[
                    scratch_card.bonus_scratch_cards_lower : scratch_card.bonus_scratch_card_upper
                ]
            ],
        )

    def load_card(self) -> list[ScratchCard]:
        filepath = os.path.join(os.path.dirname(__file__), "data.txt")
        with open(filepath, "r") as file:
            raw_txt = file.read()
        line_split = raw_txt.split("\n")
        return [self.read_line(x) for x in line_split if x != ""]

    def read_line(self, raw_line: str) -> ScratchCard:
        colon_split = raw_line.split(":")
        card_index_str = colon_split[0]
        numbers_str = colon_split[1]
        pipe_split = numbers_str.split("|")
        winning_numbers = self.extract_digits_from_str(pipe_split[0])
        numbers_you_have = self.extract_digits_from_str(pipe_split[1])
        return ScratchCard(
            card_index=int(card_index_str.replace("Card ", "")) - 1,
            winning_numbers=set(winning_numbers),
            numbers_you_have=set(numbers_you_have),
        )

    def extract_digits_from_str(self, raw_str: str) -> list[int]:
        string_split = re.sub(" +", " ", raw_str).strip().split(" ")
        return [int(x) for x in string_split]

    def compute_match(self, scratch_card: ScratchCard) -> set[int]:
        matches = scratch_card.numbers_you_have.intersection(
            scratch_card.winning_numbers
        )
        return matches


if __name__ == "__main__":
    scratch_cards = DataLoader()
    print(scratch_cards)
    print(scratch_cards.scratch_cards_with_children)
    print(scratch_cards.child_counts)
    print(sum(scratch_cards.child_counts))
