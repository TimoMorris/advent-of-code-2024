import pytest

from day_12 import day_12a, day_12b
from day_12_params import DAY_12A_PARAMS, DAY_12B_PARAMS


def get_day_12_test_input(test_case) -> list[str]:
    if test_case == "actual":
        filepath = "../src/inputs/input_12.txt"
    else:
        filepath = f"inputs/input_12_{test_case}.txt"

    with open(filepath) as f:
        contents = f.read().splitlines()

    return contents


@pytest.mark.parametrize(["test_case", "solution"], DAY_12A_PARAMS)
def test_day_12a(test_case, solution):
    test_input = get_day_12_test_input(test_case)
    result = day_12a(test_input)
    assert result == solution


@pytest.mark.parametrize(["test_case", "solution"], DAY_12B_PARAMS)
def test_day_12b(test_case, solution):
    test_input = get_day_12_test_input(test_case)
    result = day_12b(test_input)
    assert result == solution
