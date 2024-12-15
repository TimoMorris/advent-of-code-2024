def get_day_04_input() -> list[str]:
    with open("inputs/input_04.txt") as f:
        contents = f.readlines()
    return [c.strip() for c in contents]


def get_vertical_lines(horizontal_lines: list[str]) -> list[str]:
    return ["".join(x) for x in zip(*horizontal_lines)]


def get_diagonal_lines(horizontal_lines: list[str]) -> list[str]:
    length = len(horizontal_lines[0])
    height = len(horizontal_lines)

    diagonal_lines = []
    for line_total in range(length + height):
        line = "".join(horizontal_lines[row][column] for row, column in get_diagonal_indices_ne_sw(line_total, length, height))
        diagonal_lines.append(line)
    for line_difference in range(-height + 1, length):
        line = "".join(horizontal_lines[row][column] for row, column in get_diagonal_indices_nw_se(line_difference, length, height))
        diagonal_lines.append(line)
    return diagonal_lines


def get_diagonal_indices_ne_sw(line_total, length, height):
    for i in range(max(0, line_total - (length - 1)), min(line_total, height - 1) + 1):
        row = i
        column = line_total - i
        yield row, column


def get_diagonal_indices_nw_se(line_difference, length, height):
    largest = max(length, height)
    for i in range(max(0, -line_difference), min(largest, height, length - line_difference)):
        row = i
        column = line_difference + i
        yield row, column


def get_diagonal_indices_ne_sw_explicit(line_total, length, height):
    for i in range(0, line_total + 1):
        row = i
        column = line_total - i
        if row > (height - 1) or column > (length - 1):
            continue
        yield row, column


def get_diagonal_indices_nw_se_explicit(line_difference, length, height):
    largest = max(length, height)
    for i in range(0, largest):
        row = i
        column = line_difference + i
        if not 0 <= row < height or not 0 <= column < length:
            continue
        yield row, column


def search_lines(lines: list[str]) -> int:
    return sum(line.count("XMAS") for line in lines)


def search_lines_reversed(lines: list[str]) -> int:
    return sum(line[::-1].count("XMAS") for line in lines)


def day_04a(horizontal_lines: list[str]) -> int:
    searchable_lines = horizontal_lines + get_vertical_lines(horizontal_lines) + get_diagonal_lines(horizontal_lines)
    total = search_lines(searchable_lines) + search_lines_reversed(searchable_lines)
    return total


def get_cross_pairs(horizontal_lines: list[str]) -> list[tuple[str, str]]:
    length = len(horizontal_lines[0])
    height = len(horizontal_lines)

    cross_pairs = []
    for i in range(1, height - 1):
        for j in range(1, length - 1):
            x_nw_se = horizontal_lines[i - 1][j - 1] + horizontal_lines[i][j] + horizontal_lines[i + 1][j + 1]
            x_ne_sw = horizontal_lines[i - 1][j + 1] + horizontal_lines[i][j] + horizontal_lines[i + 1][j - 1]
            cross_pairs.append((x_nw_se, x_ne_sw))
    return cross_pairs


def is_cross_pair_valid(cross_pair: tuple[str, str]) -> bool:
    return all(x in ("MAS", "SAM") for x in cross_pair)


def day_04b(horizontal_lines: list[str]) -> int:
    cross_pairs = get_cross_pairs(horizontal_lines)
    total = sum(is_cross_pair_valid(cross_pair) for cross_pair in cross_pairs)
    return total


if __name__ == "__main__":
    day_04_input = get_day_04_input()
    answer_04a = day_04a(day_04_input)
    print(answer_04a)
    answer_04b = day_04b(day_04_input)
    print(answer_04b)
