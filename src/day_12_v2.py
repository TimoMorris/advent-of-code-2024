from typing import Iterable

from day_12 import get_day_12_input
from utilities.grid import Cell, Coordinates, Grid
from utilities.timer import timer


class Plot(Cell[str]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.region = Region({self}, self.coords)

    def __repr__(self):
        return f"({self.row}, {self.col}): {self.value}"


class Region:
    def __init__(self, plots: set[Plot], key: Coordinates):
        self.plots = plots
        self.key = key
        self.perimeter = 0
        self.sides = 0

    @property
    def area(self) -> int:
        return len(self.plots)

    @property
    def price(self) -> int:
        return self.area * self.perimeter

    @property
    def price_with_discount(self) -> int:
        return self.area * self.sides


NULL_PLOT = Plot(-1, -1, "")
NULL_PLOT.region = Region(set(), (-1, -1))


class Farm(Grid[Plot]):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self._regions_lookup: dict[Coordinates, Region] = {}
    
    def initialise_regions(self):
        self._regions_lookup = {plot.coords: plot.region for plot in self.all_cells()}

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:  # when trying to fetch a plot off the edge of the grid
            return NULL_PLOT

    @property
    def regions(self) -> Iterable[Region]:
        for region in self._regions_lookup.values():
            yield region

    def merge_regions(self, plot1: Plot, plot2: Plot) -> None:
        """Check if adjacent plots should belong to the same region, and if so merge them together."""
        if plot1.value != plot2.value or plot1.region is plot2.region:
            return

        plot1_region = plot1.region  # get plot1's region
        plot2_region = self._regions_lookup.pop(plot2.region.key)  # remove plot2's region from master lookup
        plot1_region.plots.update(plot2_region.plots)  # add plot2's region's plots to plot1's region
        for plot in plot2.region.plots:  # update plot2's plots to reference plot1's region
            plot.region = plot1_region


def count_borders(plot1: Plot, plot2: Plot) -> None:
    """Check if a border should exist between adjacent plots, and if so add it to the total."""
    if plot1.value != plot2.value:
        plot1.region.perimeter += 1
        plot2.region.perimeter += 1


def count_sides(previous_plot: Plot, current_plot: Plot, adjacent_plot: Plot, previous_against_side: bool) -> bool:
    """Check if a new side starts adjacent to this plot, and if so add it to the total."""
    current_against_side = current_plot.region is not adjacent_plot.region
    if current_against_side and (current_plot.region is not previous_plot.region or not previous_against_side):
        current_plot.region.sides += 1
    return current_against_side
    

@timer
def initialise_farm(grid: list[str]) -> Farm:
    farm = Farm.from_strings(grid, Plot)
    farm.initialise_regions()

    for i in range(farm.height):
        for j in range(farm.width - 1):
            farm.merge_regions(farm[i, j], farm[i, j + 1])

    for j in range(farm.width):
        for i in range(farm.height - 1):
            farm.merge_regions(farm[i, j], farm[i + 1, j])

    return farm


@timer
def day_12a_v2(farm: Farm) -> int:
    for i in range(farm.height):
        for j in range(-1, farm.width):
            count_borders(farm[i, j], farm[i, j + 1])

    for j in range(farm.width):
        for i in range(-1, farm.height):
            count_borders(farm[i, j], farm[i + 1, j])

    return sum(region.price for region in farm.regions)


@timer
def day_12b_v2(farm: Farm) -> int:
    for i in range(farm.height):
        against_side_north, against_side_south = False, False
        for j in range(farm.width):
            against_side_north = count_sides(farm[i, j - 1], farm[i, j], farm[i - 1, j], against_side_north)
            against_side_south = count_sides(farm[i, j - 1], farm[i, j], farm[i + 1, j], against_side_south)

    for j in range(farm.width):
        against_side_west, against_side_east = False, False
        for i in range(farm.height):
            against_side_west = count_sides(farm[i - 1, j], farm[i, j], farm[i, j - 1], against_side_west)
            against_side_east = count_sides(farm[i - 1, j], farm[i, j], farm[i, j + 1], against_side_east)

    return sum(region.price_with_discount for region in farm.regions)


if __name__ == "__main__":
    day_12_input = get_day_12_input()
    farm = initialise_farm(day_12_input)
    answer_12a = day_12a_v2(farm)
    print(answer_12a)
    answer_12b = day_12b_v2(farm)
    print(answer_12b)
