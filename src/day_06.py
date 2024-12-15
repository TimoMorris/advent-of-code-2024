from itertools import cycle


def get_day_06_input() -> tuple[list[list[str]], tuple[int, int]]:
    with open("inputs/input_06.txt") as f:
        contents = f.read().splitlines()

    (start_row,) = [i for i, row in enumerate(contents) if "^" in row]
    grid = [list(row) for row in contents]
    start_col = grid[start_row].index("^")
    return grid, (start_row, start_col)


DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def day_06a(grid: list[list[str]], start_pos: tuple[int, int]) -> int:
    length = len(grid[0])
    height = len(grid)

    off_grid = False
    row, col = start_pos
    grid[row][col] = "X"

    for direction_row, direction_col in cycle(DIRECTIONS):
        while True:
            next_row, next_col = row + direction_row, col + direction_col  # calculate next position
            if not (0 <= next_row < height) or not (0 <= next_col < length):  # check it's not off grid
                off_grid = True
                break
            next_item = grid[next_row][next_col]  # identify item ahead on map
            if next_item == "#":  # if obstacle, break to change direction
                break
            else:  # otherwise move ahead and mark as visited
                row, col = next_row, next_col
                grid[row][col] = "X"

        if off_grid:
            break

    # print("\n".join(" ".join(row) for row in grid), "\n")
    return sum(row.count("X") for row in grid)


def does_grid_have_cycle(grid: list[list[str]], start_pos: tuple[int, int]) -> bool:
    length = len(grid[0])
    height = len(grid)

    off_grid = False
    entered_cycle = False
    obstacles_encountered = set()
    row, col = start_pos
    grid[row][col] = "X"

    for direction in cycle(DIRECTIONS):
        dir_row, dir_col = direction
        while True:
            next_row, next_col = row + dir_row, col + dir_col  # calculate next position
            next_pos = next_row, next_col
            if not (0 <= next_row < height) or not (0 <= next_col < length):  # check it's not off grid
                off_grid = True
                break
            next_item = grid[next_row][next_col]  # identify item ahead on map
            if next_item == "#":  # if obstacle
                if (next_pos, direction) in obstacles_encountered:
                    entered_cycle = True
                else:
                    obstacles_encountered.add((next_pos, direction))
                break
            else:  # otherwise move ahead and mark as visited
                row, col = next_row, next_col
                grid[row][col] = "X"

        if off_grid:
            return False
        elif entered_cycle:
            return True


def day_06b(grid: list[list[str]], start_pos: tuple[int, int]) -> int:
    length = len(grid[0])
    height = len(grid)

    potential_obstructions = []
    for i in range(length):
        print(f"Row {i + 1:>3} of {length}")
        for j in range(height):
            if grid[i][j] not in ("#", "^"):
                grid_copy = [row[:] for row in grid]
                grid_copy[i][j] = "#"
                if does_grid_have_cycle(grid_copy, start_pos):
                    potential_obstructions.append((i, j))
    return len(potential_obstructions)



if __name__ == "__main__":
    grid, start_pos = get_day_06_input()
    answer_06a = day_06a(grid, start_pos)
    print(answer_06a)
    answer_06b = day_06b(grid, start_pos)
    print(answer_06b)
