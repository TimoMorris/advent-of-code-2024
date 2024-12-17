import time
from functools import lru_cache


def get_day_11_input() -> list[int]:
    with open("inputs/input_11.txt") as f:
        contents = f.read()

    stones = [int(x) for x in contents.split(" ")]
    return stones


def blink_stone(number: int) -> list[int]:
    """Apply the change on blinking to a single stone."""
    if number == 0:
        return [1]

    number_as_str = str(number)
    length = len(number_as_str)
    if length % 2 == 0:
        return [int(number_as_str[:length // 2]), int(number_as_str[length // 2:])]

    return [number * 2024]


def blink(stones: list[int]) -> list[int]:
    """Apply the change on blinking to all stones."""
    new_stones = []
    for stone in stones:
        new_stones.extend(blink_stone(stone))
    return new_stones


def day_11a(stones: list[int], no_blinks: int) -> int:
    tic = time.perf_counter()  # start time
    for i in range(no_blinks):
        stones = blink(stones)
    toc = time.perf_counter()  # stop time
    print(f"11a took {toc-tic:0.4f} seconds")

    no_stones = len(stones)
    return no_stones


@lru_cache(None)  # magic!
def calculate_count(stone: int, no_blinks: int) -> int:
    """Recursively calculate how many stones there will be in place of this one after the given number of blinks."""
    if no_blinks == 0:
        return 1
    return sum(calculate_count(stone, no_blinks - 1) for stone in blink_stone(stone))


def day_11b(stones: list[int], no_blinks: int) -> int:
    tic = time.perf_counter()  # start time
    total = sum(calculate_count(stone, no_blinks) for stone in stones)
    toc = time.perf_counter()  # stop time
    print(f"11b took {toc-tic:0.4f} seconds")

    return total


if __name__ == "__main__":
    day_11_input = get_day_11_input()
    answer_11a = day_11a(day_11_input, 25)
    print(answer_11a)
    answer_11b = day_11b(day_11_input, 75)
    print(answer_11b)
