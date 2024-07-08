"""
The missing part wasn't the only issue - one of the gears in the engine is wrong.
A gear is any * symbol that is adjacent to exactly two part numbers.
Its gear ratio is the result of multiplying those two numbers together.
"""

import re

from task_1 import DigitLoc, EngineSchematic, load_raw_text


class EngineSchematic2(EngineSchematic):

    def __init__(self, grid: list[list[str]], dim_x: int, dim_y: int):
        super().__init__(grid, dim_x, dim_y)
        # gears will count each gear pair twice, this doesn't matter as we can devide the sum in two
        self.star_locs = self.get_star_locs()
        self.gear_ratios = [self.get_gear_ratio(star) for star in self.star_locs]
        self.total_gear_ratios = sum(self.gear_ratios)

    @staticmethod
    def from_raw_text(raw_text: str) -> "EngineSchematic2":
        raw_text_grid = [list(row) for row in raw_text.split("\n") if row]
        dim_y = len(raw_text_grid)
        dim_x = len(raw_text_grid[0])
        return EngineSchematic2(raw_text_grid, dim_x, dim_y)

    def _clean_grid_el(self, x):
        if re.match("\d", x):
            return x
        elif x == ".":
            return "."
        elif x == "*":
            return "*"
        else:
            return "#"

    def _check_above(self, x: int, y: int) -> int:
        if y == 0:
            return []
        check_y = y - 1
        check_x = (
            ([x - 1] if x > 0 else []) + ([x]) + ([x + 1] if x < self.dim_x else [])
        )
        filtered_digits = [
            digit
            for digit in self.digit_locs
            if digit["y"] == check_y
            and any([x >= digit["start_x"] and x <= digit["end_x"] for x in check_x])
        ]
        return filtered_digits

    def _check_below(self, x: int, y: int) -> int:
        if y == self.dim_y:
            return []
        check_y = y + 1
        check_x = (
            ([x - 1] if x > 0 else []) + ([x]) + ([x + 1] if x < self.dim_x else [])
        )
        filtered_digits = [
            digit
            for digit in self.digit_locs
            if digit["y"] == check_y
            and any([x >= digit["start_x"] and x <= digit["end_x"] for x in check_x])
        ]
        return filtered_digits

    def _check_left(self, x: int, y: int) -> int:
        if x == 0:
            return []
        check_x = x - 1
        check_y = y
        return [
            digit
            for digit in self.digit_locs
            if digit["y"] == check_y and digit["end_x"] == check_x
        ]

    def _check_right(self, x: int, y: int) -> int:
        if x == self.dim_x:
            return []
        check_x = x + 1
        check_y = y
        return [
            digit
            for digit in self.digit_locs
            if digit["y"] == y and digit["start_x"] == check_x
        ]

    def get_gear_ratio(self, star: DigitLoc):
        digit_matches = []
        # check for digits above
        y = star["y"]
        x = star["start_x"]
        digits_above = self._check_above(x, y)
        digit_matches.extend(digits_above)
        digit_matches.extend(self._check_left(x, y))
        digit_matches.extend(self._check_right(x, y))
        digit_matches.extend(self._check_below(x, y))
        if len(digit_matches) == 2:
            return int(digit_matches[0]["digits"]) * int(digit_matches[1]["digits"])
        return 0

    def get_star_locs(self) -> list[DigitLoc]:
        return self.get_char_indexs("\*")


if __name__ == "__main__":
    raw_text = load_raw_text()
    engine = EngineSchematic2.from_raw_text(raw_text)
    print(engine)
    print(engine.total_gear_ratios)
