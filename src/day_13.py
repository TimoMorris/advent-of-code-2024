from enum import Enum
from math import lcm

from parse import parse

from utilities.timer import timer


class Result(Enum):
    SOLUTION = 0
    NO_INTEGER_SOLUTION = 1
    LINEARLY_DEPENDENT = 2
    CONTRADICTION = 3


type MachineConfiguration = tuple[tuple[int, int], tuple[int, int], tuple[int, int]]


def get_day_13_input() -> list[MachineConfiguration]:
    with open("inputs/input_13.txt") as f:
        contents = f.read().splitlines()
    contents.append("")

    machines = []
    i = 0
    while i < len(contents):
        a = parse("Button A: X+{:d}, Y+{:d}", contents[i])
        b = parse("Button B: X+{:d}, Y+{:d}", contents[i + 1])
        prize = parse("Prize: X={:d}, Y={:d}", contents[i + 2])
        assert contents[i + 3] == ""
        machines.append(((a[0], a[1]), (b[0], b[1]), (prize[0], prize[1])))
        i += 4
    
    return machines


def solve_machine(a: tuple[int, int], b: tuple[int, int], prize: tuple[int, int]) -> tuple[Result, tuple[int, int] | None]:
    row1 = [a[0], b[0], prize[0]]
    row2 = [a[1], b[1], prize[1]]

    target = lcm(row1[0], row2[0])
    multiplier1 = target // row1[0]
    multiplier2 = target // row2[0]

    row1 = [r1 * multiplier1 for r1 in row1]  # [x*|*]
    row2 = [r2 * multiplier2 for r2 in row2]  # [x*|*]

    row2 = [r2 - r1 for r1, r2 in zip(row1, row2)]  # [x*|*]
    assert row2[0] == 0                             # [0*|*]

    if row2[1] == 0:
        if row2[2] == 0:  # linearly dependent
            return Result.LINEARLY_DEPENDENT, None
        else:  # contradiction
            return Result.CONTRADICTION, None

    q = row2[1]
    nb, r = divmod(row2[2], q)
    if r != 0:  # no integer solution
        return Result.NO_INTEGER_SOLUTION, None
    row2 = [r2 // q for r2 in row2]  # [**|*]
                                     # [01|*]
    target = row1[1]
    row1 = [r1 - r2 * target for r1, r2 in zip(row1, row2)]  # [*0|*]
                                                             # [01|*]
    q = row1[0]
    na, r = divmod(row1[2], q)
    if r != 0:  # no integer solution
        return Result.NO_INTEGER_SOLUTION, None
    row1 = [r1 // q for r1 in row1]  # [10|*]
                                     # [01|*]
    assert a[0] * na + b[0] * nb == prize[0]
    assert a[1] * na + b[1] * nb == prize[1]

    return Result.SOLUTION, (na, nb)


@timer
def day_13a(machine_numbers: list[MachineConfiguration]) -> int:
    results = {r: 0 for r in Result}

    cost = 0
    for machine in machine_numbers:
        a, b, prize = machine
        result, solution = solve_machine(a, b, prize)
        results[result] += 1
        if result == result.SOLUTION:
            assert solution is not None
            na, nb = solution
            cost += na * 3 + nb

    for r, n in results.items():
        print(f"{r.name.replace("_", " ").title()}: {n}")

    return cost


def get_cost_v2(a: tuple[int, int], b: tuple[int, int], prize: tuple[int, int]) -> int:
    """Get the cost for the given machine via naive brute force search."""
    for i in range(101):
        for j in range(101):
            if a[0] * i + b[0] * j == prize[0] and a[1] * i + b[1] * j == prize[1]:
                return i * 3 + j
    return 0


@timer
def day_13a_v2(machine_numbers: list[MachineConfiguration]) -> int:
    cost = 0
    for machine in machine_numbers:
        a, b, prize = machine
        cost += get_cost_v2(a, b, prize)
    return cost


@timer
def day_13b(machine_numbers: list[MachineConfiguration]):
    results = {r: 0 for r in Result}

    cost = 0
    for machine in machine_numbers:
        a, b, prize = machine
        prize = (prize[0] + 10000000000000, prize[1] + 10000000000000)
        result, solution = solve_machine(a, b, prize)
        results[result] += 1
        if result == result.SOLUTION:
            assert solution is not None
            na, nb = solution
            cost += na * 3 + nb

    for r, n in results.items():
        print(f"{r.name.replace("_", " ").title()}: {n}")

    return cost


if __name__ == "__main__":
    day_13_input = get_day_13_input()
    answer_13a = day_13a(day_13_input)
    print(answer_13a)
    answer_13a_v2 = day_13a_v2(day_13_input)
    print(answer_13a_v2)
    answer_13b = day_13b(day_13_input)
    print(answer_13b)
