import itertools
import operator


def get_day_07_input() -> list[tuple[int, list[int]]]:
    with open("inputs/input_07.txt") as f:
        contents = f.read().splitlines()

    calibration_equations_as_str = [c.split(":") for c in contents]
    calibration_equations = [(int(a), [int(x) for x in b.strip().split(" ")]) for a, b in calibration_equations_as_str]
    return calibration_equations


OPERATORS = (operator.add, operator.mul)
concat_int = lambda a, b: int(str(a) + str(b))
OPERATORS_WITH_CONCAT = (operator.add, operator.mul, concat_int)


def day_07a(calibration_equations: list[tuple[int, list[int]]]) -> int:
    valid_equations = []
    for equation in calibration_equations:
        test_value, nums = equation
        for comb in itertools.product(OPERATORS, repeat=len(nums) - 1):
            result = nums[0]
            for op, n in zip(comb, nums[1:]):
                result = op(result, n)
                if result > test_value:
                    break  # overshot so break and try next operator combination
            else:  # used up all numbers and didn't overshoot
                if result == test_value:
                    valid_equations.append(equation)
                    break  # found a solution for this equation so skip any un-tried combinations and move to next equation

    return sum(test_value for test_value, nums in valid_equations)


def day_07b(calibration_equations: list[tuple[int, list[int]]]) -> int:
    valid_equations = []
    for equation in calibration_equations:
        test_value, nums = equation
        for comb in itertools.product(OPERATORS_WITH_CONCAT, repeat=len(nums) - 1):
            result = nums[0]
            for op, n in zip(comb, nums[1:]):
                result = op(result, n)
                if result > test_value:
                    break  # overshot so break and try next operator combination
            else:  # used up all numbers and didn't overshoot
                if result == test_value:
                    valid_equations.append(equation)
                    break  # found a solution for this equation so skip any un-tried combinations and move to next equation

    return sum(test_value for test_value, nums in valid_equations)


if __name__ == "__main__":
    day_07_input = get_day_07_input()
    answer_07a = day_07a(day_07_input)
    print(answer_07a)
    answer_07b = day_07b(day_07_input)
    print(answer_07b)
