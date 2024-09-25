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

def remove_double_space(a_string: str) -> str:
    return ' '.join(a_string.split())

def parse_line(line: str) -> tuple[str, list[int]]:
    colon_split = line.split(':')
    name = colon_split[0]
    value_str = remove_double_space(colon_split[1])
    print(value_str)
    values = [int(v) for v in value_str.split()]
    return name, values

def create_boat_distances(race_length: int) -> list[BoatDistance]:
    return [
        BoatDistance(
            seconds_down=seconds_down,
            distance_travelled=seconds_down * (race_length - seconds_down),
            race_length=race_length
        )
        for seconds_down in range(race_length)
    ]


    
def main():
    data = load_data()
    race_boat_distances = [
        create_boat_distances(time_distance.time)
        for time_distance in data

    ]
    number_of_solutions = [
        sum(boat_distance.distance_travelled>time_distance.distance for boat_distance in boat_distances)
        for time_distance, boat_distances in zip(data, race_boat_distances)
    ]
    print(data)
    print(number_of_solutions)
    print(f"Solution: {math.prod(number_of_solutions)}")
    
if __name__ == '__main__':
    main()
