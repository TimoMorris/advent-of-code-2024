from collections import deque
from enum import Enum
from typing import Callable

from utilities.grid import Cell, Coordinates, Grid, STRAIGHT_VECTORS
from utilities.timer import timer


def get_day_12_input() -> list[str]:
    with open("inputs/input_12.txt") as f:
        contents = f.read().splitlines()

    return contents


class Side(Enum):
    UNKNOWN = 0
    CONNECTED = 1
    BORDER = 2


class Plot(Cell[str]):
    def __init__(self, row: int, col: int, crop: str, *, grid=None):
        super().__init__(row, col, crop, grid=grid)
        self.sides: dict[Coordinates, Side] = {
            (0, 1): Side.UNKNOWN,
            (1, 0): Side.UNKNOWN,
            (0, -1): Side.UNKNOWN,
            (-1, 0): Side.UNKNOWN,
        }

    def __repr__(self):
        return f"({self.row}, {self.col}): {self.crop}"

    @property
    def crop(self) -> str:
        return self.value

    @property
    def border_count(self):
        return len([side for side in self.sides.values() if side == Side.BORDER])


class Farm(Grid[Plot]):

    @property
    def plots(self) -> set[Plot]:
        return set(self._cells.values())


class Boundary:
    def __init__(self, border_pieces: list[tuple[Coordinates, Coordinates]]):
        self.border_pieces: list[tuple[Coordinates, Coordinates]] = border_pieces
        self.directions: list[Coordinates] = [direction for __, direction in self.border_pieces]

    @property
    def side_count(self) -> int:
        sides = 0
        for i in range(len(self.border_pieces)):
            if self.directions[i - 1] != self.directions[i]:
                sides += 1
        return sides


class Region:
    def __init__(self, plots: set[Plot], boundaries: list[Boundary] | None = None):
        self.plots: set[Plot] = plots
        self.boundaries: list[Boundary] = boundaries or []

    @property
    def area(self) -> int:
        return len(self.plots)

    @property
    def perimeter(self) -> int:
        return sum(plot.border_count for plot in self.plots)

    @property
    def price(self) -> int:
        return self.area * self.perimeter

    @property
    def sides(self) -> int:
        return sum(boundary.side_count for boundary in self.boundaries)

    @property
    def price_with_discount(self) -> int:
        return self.area * self.sides


def is_part_of_region(new_plot: Plot, parent_plot: Plot) -> bool:
    return new_plot.crop == parent_plot.crop


def mark_as_part_of_region(new_plot: Plot, parent_plot: Plot) -> None:
    direction = new_plot - parent_plot
    parent_plot.sides[direction] = Side.CONNECTED


def mark_as_border(new_plot: Plot, parent_plot: Plot) -> None:
    direction = new_plot - parent_plot
    parent_plot.sides[direction] = Side.BORDER


def find_region(
    unsearched_plots: set[Plot],
    can_connect: Callable[[Plot, Plot], bool] = is_part_of_region,
    connect: Callable[[Plot, Plot], None] = mark_as_part_of_region,
    unconnect: Callable[[Plot, Plot], None] = mark_as_border
) -> set[Plot]:
    starting_plot = unsearched_plots.pop()
    search_queue: deque[Plot] = deque([starting_plot])
    region: set[Plot] = {starting_plot}
    out_of_region: set[Plot] = set()

    while search_queue:
        current_plot = search_queue.popleft()
        for adj_plot in current_plot.get_adjacent_cells():
            unsearched = adj_plot in unsearched_plots
            if unsearched:
                unsearched_plots.remove(adj_plot)
            if can_connect(adj_plot, current_plot):
                connect(adj_plot, current_plot)
                region.add(adj_plot)
                if unsearched:
                    search_queue.append(adj_plot)
            else:
                unconnect(adj_plot, current_plot)
                out_of_region.add(current_plot)

    return region


def mark_outer_border(farm: Farm):
    for x in range(farm.width):
        farm[0, x].sides[-1, 0] = Side.BORDER
        farm[farm.height - 1, x].sides[1, 0] = Side.BORDER
    for x in range(farm.height):
        farm[x, 0].sides[0, -1] = Side.BORDER
        farm[x, farm.height - 1].sides[0, 1] = Side.BORDER


def identify_regions(farm: Farm) -> list[Region]:
    unallocated_plots: set[Plot] = farm.plots

    regions = []
    while unallocated_plots:
        region = find_region(unallocated_plots.copy())
        regions.append(Region(region))
        unallocated_plots -= region
    mark_outer_border(farm)

    return regions


@timer
def day_12a(grid: list[str]) -> int:
    farm = Farm.from_strings(grid, Plot)
    regions = identify_regions(farm)

    return sum(region.price for region in regions)


class BoundaryWalker:
    def __init__(self, region, farm):
        self.region = region
        self.farm = farm
        self.unconnected_border_pieces = set(
            (plot.coords, direction) for plot in self.region.plots for direction, side in plot.sides.items()
            if side == Side.BORDER
        )
        self.boundaries = []
        self.current_direction: Coordinates | None = None
        self.current_plot: Plot | None = None
        self.boundary: list[tuple[Coordinates, Coordinates]] = []

    @staticmethod
    def rotate_clockwise(direction: Coordinates, turns=1) -> Coordinates:
        idx = STRAIGHT_VECTORS.index(direction)
        return STRAIGHT_VECTORS[(idx + turns) % 4]

    @staticmethod
    def rotate_anticlockwise(direction: Coordinates, turns=1) -> Coordinates:
        idx = STRAIGHT_VECTORS.index(direction)
        return STRAIGHT_VECTORS[(idx - turns) % 4]

    @property
    def current_left(self) -> Coordinates:
        return self.rotate_anticlockwise(self.current_direction)

    def border_turns_right(self) -> tuple[Coordinates, Coordinates] | None:
        if self.current_plot.sides[self.current_direction] == Side.BORDER:
            border_piece = (self.current_plot.coords, self.current_direction)
            return border_piece

    def border_continues_ahead(self) ->  tuple[Coordinates, Coordinates] | None:
        plot_ahead = self.current_plot + self.current_direction
        if plot_ahead.sides[self.current_left] == Side.BORDER:
            border_piece = (plot_ahead.coords, self.current_left)
            return border_piece

    def border_turns_left(self) ->  tuple[Coordinates, Coordinates] | None:
        plot_ahead_left = self.current_plot + self.current_direction + self.current_left
        current_left_left = self.rotate_anticlockwise(self.current_direction, 2)
        if plot_ahead_left.sides[current_left_left] == Side.BORDER:
            border_piece = (plot_ahead_left.coords, current_left_left)
            return border_piece

    def turn_right(self):
        self.current_direction = self.rotate_clockwise(self.current_direction)

    def move_ahead(self):
        self.current_plot = self.current_plot + self.current_direction

    def move_ahead_and_left(self):
        self.current_plot = self.current_plot + self.current_direction + self.current_left
        self.current_direction = self.current_left

    def add_to_current_boundary(self, border_piece: tuple[Coordinates, Coordinates]) -> None:
        self.unconnected_border_pieces.remove(border_piece)
        self.boundary.append(border_piece)

    def walk(self) -> list[Boundary]:
        while self.unconnected_border_pieces:
            starting_border_piece = self.unconnected_border_pieces.pop()
            self.boundary = [starting_border_piece]

            starting_coords, starting_border = starting_border_piece
            self.current_plot = self.farm[starting_coords]
            self.current_direction = self.rotate_clockwise(starting_border)

            while True:
                if border_piece := self.border_turns_right():
                    self.turn_right()
                elif border_piece := self.border_continues_ahead():
                    self.move_ahead()
                elif border_piece := self.border_turns_left():
                    self.move_ahead_and_left()
                else:
                    raise ValueError("Unexpected border configuration encountered.")

                if border_piece == starting_border_piece:
                    break

                self.add_to_current_boundary(border_piece)

            self.boundaries.append(Boundary(self.boundary))

        return self.boundaries


@timer
def day_12b(grid: list[str]) -> int:
    farm = Farm.from_strings(grid, Plot)
    regions = identify_regions(farm)

    for region in regions:
        region.boundaries = BoundaryWalker(region, farm).walk()

    return sum(region.price_with_discount for region in regions)


if __name__ == "__main__":
    day_12_input = get_day_12_input()
    answer_12a = day_12a(day_12_input)
    print(answer_12a)
    answer_12b = day_12b(day_12_input)
    print(answer_12b)
