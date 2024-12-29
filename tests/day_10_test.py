import pytest

from day_10 import day_10a, day_10b
from day_10_params import DAY_10A_PARAMS, DAY_10B_PARAMS


def get_day_10_test_input(test_case) -> list[list[int]]:
    if test_case == "actual":
        filepath = "../src/inputs/input_10.txt"
    else:
        filepath = f"inputs/input_10_{test_case}.txt"

    with open(filepath) as f:
        contents = f.read().splitlines()

    grid = [[99 if x == "." else int(x) for x in line] for line in contents]
    return grid


@pytest.mark.parametrize(["test_case", "solution"], DAY_10A_PARAMS)
def test_day_10a(test_case, solution):
    test_input = get_day_10_test_input(test_case)
    result = day_10a(test_input)
    assert result == solution


@pytest.mark.parametrize(["test_case", "solution"], DAY_10B_PARAMS)
def test_day_10b(test_case, solution):
    test_input = get_day_10_test_input(test_case)
    result = day_10b(test_input)
    assert result == solution
