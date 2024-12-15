import itertools
from collections import defaultdict
from dataclasses import dataclass
from math import gcd
from typing import Union


@dataclass
class Location:
    """Class for a position on the map, specified by row and column.

    Supports:
    - addition with a Vector
    - subtraction with another Location to give the Vector between them
    - hashable (for use in sets)
    - is_on_map() with a supplied grid length and height to check whether a position is on the map

    """
    row: int
    col: int

    def __add__(self, other: "Vector") -> "Location":
        return Location(self.row + other.row, self.col + other.col)

    def __sub__(self, other: "Location") -> "Vector":
        return Vector(self.row - other.row, self.col - other.col)

    def __hash__(self) -> int:
        return hash((self.__class__, self.row, self.col))

    def is_on_map(self, length: int, height: int) -> bool:
        return 0 <= self.row < height and 0 <= self.col < length


@dataclass
class Vector:
    """Class for a directional vector, specified by row and column.

    Supports:
    - addition with other Vectors and Locations
    - subtraction with other Vectors
    - multiplication by an integer constant
    - dividing by an integer constant (must be a factor of both coordinates, i.e. resulting in integer coordinates)
    - negation, to give a vector pointing in the opposite direction

    """
    row: int
    col: int

    def __add__(self, other: Union["Vector", "Location"]) -> Union["Vector", "Location"]:
        if isinstance(other, Vector):
            return Vector(self.row + other.row, self.col + other.col)
        elif isinstance(other, Location):
            return Location(self.row + other.row, self.col + other.col)
        else:
            return NotImplemented

    def __sub__(self, other: "Vector") -> "Vector":
        if isinstance(other, Vector):
            return Vector(self.row - other.row, self.col - other.col)
        else:
            return NotImplemented

    def __mul__(self, other: int) -> "Vector":
        if isinstance(other, int):
            return Vector(self.row * other, self.col * other)
        else:
            return NotImplemented

    def __floordiv__(self, other: int) -> "Vector":
        if isinstance(other, int):
            row_quotient, row_remainder = divmod(self.row, other)
            if row_remainder != 0:
                raise ValueError("Divisor must be factor of row coordinate")
            col_quotient, col_remainder = divmod(self.col, other)
            if col_remainder != 0:
                raise ValueError("Divisor must be factor of column coordinate")
            return Vector(row_quotient, col_quotient)
        else:
            return NotImplemented

    def __neg__(self):
        return Vector(-self.row, -self.col)



def get_day_08_input() -> list[str]:
    with open("inputs/input_08.txt") as f:
        contents = f.read().splitlines()

    return contents


def get_locations_by_frequency(map: list[str]) -> dict[str, list[Location]]:
    locations_by_frequency = defaultdict(list)
    
    length = len(map[0])
    height = len(map)
    for i in range(height):
        for j in range(length):
            if map[i][j] != ".":
                locations_by_frequency[map[i][j]].append(Location(i, j))
    
    return dict(locations_by_frequency)

    
def get_antinodes(antenna_1: Location, antenna_2: Location, length: int, height: int) -> list[Location]:
    """Get antinodes for a pair of antennae."""

    vector_1_to_2 = antenna_2 - antenna_1
    antinode_beyond_2 = antenna_2 + vector_1_to_2
    vector_2_to_1 = antenna_1 - antenna_2
    antinode_beyond_1 = antenna_1 + vector_2_to_1

    antinodes = [antinode for antinode in [antinode_beyond_2, antinode_beyond_1] if antinode.is_on_map(length, height)]
    return antinodes

def day_08a(map: list[str]):
    locations_by_frequency = get_locations_by_frequency(map)

    length = len(map[0])
    height = len(map)
    
    antinodes = set()
    for frequency, locations in locations_by_frequency.items():
        for a, b in itertools.combinations(locations, 2):
            antinodes.update(get_antinodes(a, b, length, height))

    return len(antinodes)


def get_possible_steps(start: Location, direction: Vector, length: int, height: int) -> int:
    """Work out how many steps we can take in `direction` from `start` while remaining on the grid."""

    if direction.row < 0:  # if negative, will be heading towards top
        possible_steps_row_wise = start.row // abs(direction.row)
    else:  # if positive, will be heading towards bottom
        possible_steps_row_wise = (height - 1 - start.row) // direction.row

    if direction.col < 0:  # if negative, will be heading towards left
        possible_steps_col_wise = start.col // abs(direction.col)
    else:  # if positive, will be heading towards right
        possible_steps_col_wise = (length - 1 - start.col) // direction.col

    possible_steps = min(possible_steps_row_wise, possible_steps_col_wise)
    return possible_steps


def get_antinodes_with_harmonics(antenna_1: Location, antenna_2: Location, length: int, height: int) -> list[Location]:
    """Get antinodes for a pair of antennae, taking resonant harmonics into account."""

    vector_1_to_2 = antenna_2 - antenna_1
    highest_factor = gcd(vector_1_to_2.row, vector_1_to_2.col)
    smallest_step = vector_1_to_2 // highest_factor

    low = get_possible_steps(antenna_1, -smallest_step, length, height)  # possible steps from antenna_1 away from antenna_2
    high = get_possible_steps(antenna_1, smallest_step, length, height)  # possible steps from antenna_1 towards antenna_2 (and beyond)

    antinodes = [antenna_1 + smallest_step * i for i in range(-low, high + 1)]
    assert antenna_2 in antinodes
    return antinodes


def day_08b(map: list[str]):
    locations_by_frequency = get_locations_by_frequency(map)

    length = len(map[0])
    height = len(map)

    antinodes = set()
    for frequency, locations in locations_by_frequency.items():
        for a, b in itertools.combinations(locations, 2):
            antinodes.update(get_antinodes_with_harmonics(a, b, length, height))

    return len(antinodes)



if __name__ == "__main__":
    day_08_input = get_day_08_input()
    answer_08a = day_08a(day_08_input)
    print(answer_08a)
    answer_08b = day_08b(day_08_input)
    print(answer_08b)
