def get_day_00_input() -> list[str]:
    with open("inputs/input_00_example.txt") as f:
        contents = f.read().splitlines()
    
    return contents


def day_00a():
    pass


# def day_00b():
#     pass


if __name__ == "__main__":
    day_00_input = get_day_00_input()
    answer_00a = day_00a(day_00_input)
    print(answer_00a)
    # answer_00b = day_00b(day_00_input)
    # print(answer_00b)
