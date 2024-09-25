import os
from dataclasses import dataclass
from rich import print
import math

@dataclass
class TimeDistance:
    time: int
    distance: int

@dataclass
class BoatDistance:
    seconds_down: int
    distance_travelled: int
    race_length: int
    winner: bool


def load_data() -> list[TimeDistance]:
    filepath = os.path.join(os.path.dirname(__file__), 'data.txt')
    with open(filepath, 'r') as file:
        raw_data = file.read()

    lines = [x for x in raw_data.split('\n') if x]
    parsed_lines = [parse_line(line) for line in lines]
    time_values = next(t[1] for t in parsed_lines if t[0] == 'Time')
    distance_values = next(t[1] for t in parsed_lines if t[0] == 'Distance')
    assert len(time_values) == len(distance_values), "oh, shucks the values should match"
    return [TimeDistance(time, distance) for time, distance in zip(time_values, distance_values)]

def remove_all_spaces(a_string: str) -> str:
    return ''.join(a_string.split())

def parse_line(line: str) -> tuple[str, list[int]]:
    colon_split = line.split(':')
    name = colon_split[0]
    value_str = remove_all_spaces(colon_split[1])
    values = [int(v) for v in value_str.split()]
    return name, values

def create_boat_distances(race_length: int, winning_distance: int) -> list[BoatDistance]:
    return [
        BoatDistance(
            seconds_down=seconds_down,
            distance_travelled=seconds_down * (race_length - seconds_down),
            winner=seconds_down * (race_length - seconds_down) > winning_distance,
            race_length=race_length
        )
        for seconds_down in range(race_length)
    ]

def compute_num_wins(race_length: int, current_best: int) -> int:
    """
    problem:
    when is the polynomial:
        t*race_length - t**2 - current_best > 0
    for t in the range 0 to race_length.
    roots:
        (- b +/- sqrt(b**2 - 4ac)) / 2a
    =   (-race_length +- sqrt(race_length**2 - 4*current_best)) / (-2)
    """
    root_1 =  (-race_length + math.sqrt(race_length**2 - 4*current_best)) / (-2)
    root_2 =  (-race_length - math.sqrt(race_length**2 - 4*current_best)) / (-2)
    if root_1 < root_2:
        min_val = math.ceil(root_1)
        max_val = math.floor(root_2) + 1
    else:
        min_val = math.ceil(root_2)
        max_val = math.floor(root_1) + 1
    print(min_val, max_val)
    num_ways_to_win = (max_val - min_val)
    return num_ways_to_win


def main():
    data = load_data()
    print(data)
    num_ways_to_win = [compute_num_wins(d.time, d.distance) for d in data]
    print(num_ways_to_win)
    print(math.prod(num_ways_to_win))
    
if __name__ == '__main__':
    main()
