from collections import deque
from enum import Enum
from typing import Callable

from utilities.grid import Cell, Coordinates, Grid
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


class Region:
    def __init__(self, plots: set[Plot]):
        self.plots: set[Plot] = plots

    @property
    def area(self) -> int:
        return len(self.plots)

    @property
    def perimeter(self) -> int:
        return sum(plot.border_count for plot in self.plots)

    @property
    def price(self) -> int:
        return self.area * self.perimeter


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


@timer
def day_12a(grid: list[str]):
    farm = Farm.from_strings(grid, Plot)
    unallocated_plots: set[Plot] = farm.plots

    regions = []
    while unallocated_plots:
        region = find_region(unallocated_plots.copy())
        regions.append(Region(region))
        unallocated_plots -= region
    mark_outer_border(farm)

    return sum(region.area * region.perimeter for region in regions)


if __name__ == "__main__":
    day_12_input = get_day_12_input()
    answer_12a = day_12a(day_12_input)
    print(answer_12a)
