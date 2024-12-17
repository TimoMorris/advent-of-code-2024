from dataclasses import dataclass, field


def get_day_10_input() -> list[list[int]]:
    with open("inputs/input_10.txt") as f:
        contents = f.read().splitlines()

    grid = [[int(x) for x in line] for line in contents]
    return grid


NESW = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # cardinal direction offsets


@dataclass
class Point:
    """A point on the map."""
    row: int
    col: int
    height: int
    reachable_summits: set["Point"] = field(default_factory=set)
    trails: set["Trail"] = field(default_factory=set)

    def __hash__(self):
        return hash((self.row, self.col))

    def __repr__(self):
        return f"Point({self.row}, {self.col})"


class Map:
    """The map comprising a grid of points, each with a height."""
    def __init__(self, grid: list[list[int]]) -> None:
        self.height = len(grid)
        self.width = len(grid[0])
        self.points: dict[tuple[int, int], Point] = self.initialise_map(grid)

    @staticmethod
    def initialise_map(grid: list[list[int]]) -> dict[tuple[int, int], Point]:
        """Initialise the map points based on a grid of numbers."""
        points: dict[tuple[int, int], Point] = {}
        for row_no, row in enumerate(grid):
            for col_no, height in enumerate(row):
                points[(row_no, col_no)] = Point(row_no, col_no, height)
        return points

    def get_adjacent_points(self, point: Point, height: int | None = None) -> list[Point]:
        """Get the points adjacent to the given one, optionally specifying a required height."""
        current_row, current_col = point.row, point.col

        adjacent_points = []
        for row_offset, col_offset in NESW:
            new_row = current_row + row_offset
            new_col = current_col + col_offset
            if 0 <= new_row < self.height and 0 <= new_col < self.width:
                adjacent_points.append(self.points[(new_row, new_col)])

        if height is not None:
            adjacent_points = [point for point in adjacent_points if point.height == height]

        return adjacent_points

    def get_all_points(self, height: int) -> list[Point]:
        """Get all the points on the map with the given height."""
        return [point for point in self.points.values() if point.height == height]


def day_10a(grid: list[list[int]]) -> int:
    topographic_map = Map(grid)

    summits = topographic_map.get_all_points(9)
    for summit in summits:
        summit.reachable_summits.add(summit)

    summitable_points = set(summits)  # set of points of the current height that have a trail to at least one summit
    for height in reversed(range(0, 9)):
        adjacent_summitable_points = set()
        for point in summitable_points:
            for adjacent_point in topographic_map.get_adjacent_points(point, height):  # get adjacent points at the new height (ie the next one down)
                # this point might be adjacent to multiple points from the previous height, with trails to different sets of summits
                # using `.update()` (rather than assigning) means we combine these all together
                adjacent_point.reachable_summits.update(point.reachable_summits)
                adjacent_summitable_points.add(adjacent_point)  # add this point to the set of points at this height that have a trail to a summit
        summitable_points = adjacent_summitable_points.copy()  # the points reached at this level become the starting points for the next level down

    trailhead_score_total = sum(len(point.reachable_summits) for point in summitable_points)
    return trailhead_score_total


class Trail:
    def __init__(self, start_point: Point):
        self.route: list[tuple[int, int]] = [(start_point.row, start_point.col)]

    def add(self, point: Point) -> "Trail":
        self.route.append((point.row, point.col))
        return self

    def __hash__(self):
        return hash(tuple(self.route))

    def __repr__(self):
        return str(self.route)


def day_10b(grid: list[list[int]]) -> int:
    topographic_map = Map(grid)

    summits = topographic_map.get_all_points(9)
    for summit in summits:
        summit.trails.add(Trail(summit))

    summitable_points = set(summits)
    for height in reversed(range(0, 9)):
        adjacent_summitable_points = set()
        for point in summitable_points:
            for adjacent_point in topographic_map.get_adjacent_points(point, height):
                adjacent_point.trails.update(trail.add(adjacent_point) for trail in point.trails)
                adjacent_summitable_points.add(adjacent_point)
        summitable_points = adjacent_summitable_points.copy()

    trailhead_rating_total = sum(len(point.trails) for point in summitable_points)
    return trailhead_rating_total


if __name__ == "__main__":
    day_10_input = get_day_10_input()
    answer_10a = day_10a(day_10_input)
    print(answer_10a)
    answer_10b = day_10b(day_10_input)
    print(answer_10b)
