from math import prod

from parse import parse

from utilities.timer import timer

type Vector = tuple[int, int]
type Robot = tuple[Vector, Vector]

def get_day_14_input() -> tuple[list[Robot], Vector]:
    dimensions = (101, 103)
    with open("inputs/input_14.txt") as f:
        contents = f.read().splitlines()

    parsed = [parse("p={:d},{:d} v={:d},{:d}", line) for line in contents]
    robots = [((px, py), (vx, vy)) for px, py, vx, vy in parsed]
    return robots, dimensions


def move_robot(robot: Robot, seconds: int, width: int, height: int) -> Vector:
    ((px, py), (vx, vy)) = robot
    x = (px + vx * seconds) % width
    y = (py + vy * seconds) % height
    return x, y


def get_quadrant(x: int, y: int, half_width: int, half_height: int) -> tuple[bool | None, bool | None]:
    qx = None if x == half_width else x > half_width
    qy = None if y == half_height else y > half_height
    return qx, qy


@timer
def day_14a(robots: list[Robot], dimensions: Vector) -> int:
    width, height = dimensions
    half_width = width // 2
    half_height = height // 2

    quadrants = {(qx, qy): 0 for qx in (False, None, True) for qy in (False, None, True)}
    for robot in robots:
        x, y = move_robot(robot, 100, width, height)
        qx, qy = get_quadrant(x, y, half_width, half_height)
        quadrants[(qx, qy)] += 1

    assert sum(quadrants.values()) == len(robots)

    safety_factor = prod(quadrants[a, b] for a in (False, True) for b in (False, True))
    return safety_factor


def show_positions(positions: set[Vector], width, height) -> None:
    for j in range(height):
        print("".join("*" if (i, j) in positions else "." for i in range(width)))


@timer
def day_14b(robots: list[Robot], dimensions: Vector):
    width, height = dimensions

    for s in range(1_000_000):
        positions = set(move_robot(robot, s, width, height) for robot in robots)

        for a, b in positions:
            if all((a + i, b + j) in positions for i in (-1, 0, 1) for j in (-1, 0, 1)):
                show_positions(positions, width, height)
                return s


if __name__ == "__main__":
    day_14_input = get_day_14_input()
    answer_14a = day_14a(*day_14_input)
    print(answer_14a)
    answer_14b = day_14b(*day_14_input)
    print(answer_14b)
