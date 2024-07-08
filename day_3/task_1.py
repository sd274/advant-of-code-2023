import os
import re
from typing import TypedDict


class DigitLoc(TypedDict):
    y: int
    x_start: int
    y_start: int
    digits: str


def load_raw_text() -> str:
    filepath = os.path.join(os.path.dirname(__file__), "data.txt")
    with open(filepath, "r") as file:
        raw_text = file.read()
    return raw_text


class EngineSchematic:
    grid: list[list[str]]
    max_x: int
    max_y: int

    def __init__(self, grid: list[list[str]], dim_x: int, dim_y: int):
        self._validate_inputs(grid, dim_x, dim_y)
        self.grid = self._clean_grid(grid)
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.digit_locs = self.get_digit_indexs()
        self.symbol_locs = self.get_symbol_indexs()
        self.parts = [x for x in self.digit_locs if self.check_index_for_neighbour(x)]
        self.total_sum = sum([int(x["digits"]) for x in self.parts])

    @staticmethod
    def from_raw_text(raw_text: str) -> "EngineSchematic":
        raw_text_grid = [list(row) for row in raw_text.split("\n") if row]
        dim_y = len(raw_text_grid)
        dim_x = len(raw_text_grid[0])
        return EngineSchematic(raw_text_grid, dim_x, dim_y)

    def _validate_inputs(self, grid: list[list[str]], dim_x: int, dim_y: int):
        assert len(grid) == dim_y, "There should be y lists in the grid"
        assert all(
            [len(x) == dim_x for x in grid]
        ), f"Each row of the grid should have {dim_x} elms"
        assert all([len(x) == 1 for y in grid for x in y])

    def _clean_grid_el(self, x):
        if re.match("\d", x):
            return x
        if x == ".":
            return "."
        else:
            return "#"

    def _clean_grid(self, grid: list[list[str]]) -> list[list[str]]:
        return [[self._clean_grid_el(x) for x in y] for y in grid]

    def __str__(self):
        grid = self.grid
        res = ""
        for row in grid:
            for el in row:
                res += el
            res += "\n"
        return res

    def get_char_indexs(self, pattern: str) -> list[DigitLoc]:
        grid = self.grid
        digit_locs = []
        for y_idx, row in enumerate(grid):
            start = None
            end = None
            digits = ""
            for x_idx, el in enumerate(row):
                if start is not None:
                    if re.match(pattern, el):
                        digits += el
                        end = x_idx
                        if x_idx == self.dim_x - 1:
                            digit_locs.append(
                                {
                                    "y": y_idx,
                                    "start_x": start,
                                    "end_x": end,
                                    "digits": digits,
                                }
                            )
                            start = None
                            end = None
                            digits = ""
                    else:
                        digit_locs.append(
                            {
                                "y": y_idx,
                                "start_x": start,
                                "end_x": end,
                                "digits": digits,
                            }
                        )
                        start = None
                        end = None
                        digits = ""
                elif start is None:
                    if re.match(pattern, el):
                        start = x_idx
                        end = x_idx
                        digits += el
        return digit_locs

    def get_digit_indexs(self) -> list[DigitLoc]:
        return self.get_char_indexs("\d")

    def get_symbol_indexs(self) -> list[DigitLoc]:
        return self.get_char_indexs("#")

    def _check_for_symbol(self, check_x: int, check_y: int):
        filtered_symbols = [
            x for x in self.symbol_locs if x["start_x"] == check_x and x["y"] == check_y
        ]
        return len(filtered_symbols) > 0

    def check_index_for_neighbour(self, digit_loc: DigitLoc):
        y = digit_loc["y"]
        start_x = digit_loc["start_x"]
        end_x = digit_loc["end_x"]
        # check for symbol to the left
        check_x = max(start_x - 1, 0)
        check_y = y
        if self._check_for_symbol(check_x, check_y):
            return True
        # check to the right
        check_x = min(end_x + 1, self.dim_x)
        check_y = y
        if self._check_for_symbol(check_x, check_y):
            return True
        # check under
        if y < self.dim_y:
            check_y = y + 1
            for check_x in range(start_x, end_x + 1):
                if self._check_for_symbol(check_x, check_y):
                    return True

        if y > 0:
            check_y = y - 1
            for check_x in range(start_x, end_x + 1):
                if self._check_for_symbol(check_x, check_y):
                    return True

        # check the four diagonals
        if y > 0:
            check_y = y - 1
            if start_x > 0:
                check_x = start_x - 1
                if self._check_for_symbol(check_x, check_y):
                    return True
            if end_x < self.dim_x:
                check_x = end_x + 1
                if self._check_for_symbol(check_x, check_y):
                    return True
        if y < self.dim_y:
            check_y = y + 1
            if start_x > 0:
                check_x = start_x - 1
                if self._check_for_symbol(check_x, check_y):
                    return True
            if end_x < self.dim_x:
                check_x = end_x + 1
                if self._check_for_symbol(check_x, check_y):
                    return True
        return False


if __name__ == "__main__":
    raw_text = load_raw_text()
    print(raw_text)
    engine = EngineSchematic.from_raw_text(raw_text)
    print(engine)
    for indx in engine.digit_locs:
        print(indx)
        print(engine.check_index_for_neighbour(indx))
    print(engine.total_sum)
