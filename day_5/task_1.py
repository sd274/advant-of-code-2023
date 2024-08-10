import os
from dataclasses import dataclass
from typing import Literal, Union
from rich import print

Things = Literal[
    "seed",
    "soil",
    "fertilizer",
    "water",
    "light",
    "temperature",
    "humidity",
    "location",
]


@dataclass
class ThingMap:
    map_from: Things
    map_to: Things
    from_range_start: int
    to_range_start: int
    range_length: int

    def from_map_to_value(
        self, map_from: str, value: int
    ) -> Union[tuple[Things, int], None]:
        if map_from != self.map_from:
            return None
        print(
            f"value: {value}, from_range_start: {self.from_range_start}, range_length: {self.range_length}"
        )
        if (
            value >= self.from_range_start
            and value < self.from_range_start + self.range_length
        ):
            return self.map_to, self.to_range_start + (value - self.from_range_start)
        return None


class Task:

    def __init__(self):
        seed_list, thing_maps = self.load_data()
        self.seed_list = seed_list
        self.thing_map = thing_maps
        for seed in seed_list:
            res = [thing.from_map_to_value("seed", seed) for thing in self.thing_map]
            print(res)

    def load_data(self) -> tuple[list[int], list[ThingMap]]:
        filepath = os.path.join(os.path.dirname(__file__), "data.txt")
        with open(filepath, "r") as file:
            raw_text = file.read()
        processed = self._process_raw(raw_text)
        return processed

    def _process_raw(self, raw_text: str) -> tuple[list[int], list[ThingMap]]:
        chunks = raw_text.split("\n\n")
        chunk_splits = [chunk.split(":") for chunk in chunks]
        seed_list_str = next(
            chunk_split[1] for chunk_split in chunk_splits if chunk_split[0] == "seeds"
        )
        assert seed_list_str is not None, "uh oh issue with the seeds"
        seed_list = [int(x) for x in seed_list_str.split(" ") if x]
        maps = [(x[0], x[1]) for x in chunk_splits if "map" in x[0]]
        things = self._process_thing_strs(maps)
        return seed_list, things

    def _process_thing_strs(self, maps: list[tuple[str, str]]) -> list[ThingMap]:
        return [
            processed_map
            for map in maps
            for processed_map in self._process_thing_str(map)
        ]

    def _process_range_str(self, x: str) -> tuple[int, int, int]:
        x_list = x.split(" ")
        assert len(x_list) == 3, f"Oh fuck, Expected list of len 2, recieved {x}"
        x_list_int = [int(x) for x in x_list]
        return (x_list_int[0], x_list_int[1], x_list_int[2])

    def _process_thing_str(self, map: tuple[str, str]) -> list[ThingMap]:
        from_to_str = map[0].replace(" map", "")
        from_to_split = from_to_str.split("-to-")
        from_str = from_to_split[0]
        to_str = from_to_split[1]
        ranges = [self._process_range_str(x) for x in map[1].split("\n") if x]
        return [
            ThingMap(
                map_to=to_str,  # pyright: ignore
                map_from=from_str,  # pyright: ignore
                from_range_start=range[0],
                to_range_start=range[1],
                range_length=range[2],
            )
            for range in ranges
        ]


if __name__ == "__main__":
    task = Task()
