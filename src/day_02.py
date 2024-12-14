def get_day_02_input() -> list[list[int]]:
    with open("inputs/input_02.txt") as f:
        contents = f.readlines()

    reports = [[int(x) for x in line.split(" ")] for line in contents]
    return reports


def is_report_safe(report):
    steps = [level2 - level1 for level1, level2 in zip(report[:-1], report[1:])]
    increasing = all(step in (1, 2, 3) for step in steps)
    decreasing = all(step in (-1, -2, -3) for step in steps)
    is_safe = decreasing or increasing
    return is_safe


def day_02a(reports: list[list[int]]) -> int:
    return sum(
        (
            all(
                level1 - level2 in (1, 2, 3)
                for level1, level2 in zip(report[:-1], report[1:])
            )
            or all(
                level1 - level2 in (-1, -2, -3)
                for level1, level2 in zip(report[:-1], report[1:])
            )
        )
        for report in reports
    )


def get_modified_reports(report: list[int]) -> list[list[int]]:
    modified_reports = []
    for remove in range(len(report)):
        modified_report = [level for i, level in enumerate(report) if i != remove]
        modified_reports.append(modified_report)
    return modified_reports


def day_02b(reports: list[list[int]]) -> int:
    statuses = []
    for report in reports:
        is_safe = is_report_safe(report)
        if is_safe:
            statuses.append(True)
        elif any(is_report_safe(mr) for mr in get_modified_reports(report)):
            statuses.append(True)
        else:
            statuses.append(False)
    return sum(statuses)


def day_02b_one_line_with_safe_function(reports: list[list[int]]) -> int:
    return sum(
        is_report_safe(report)
        or any(
            is_report_safe(mr)
            for mr in [
                [level for i, level in enumerate(report) if i != remove]
                for remove in range(len(report))
            ]
        )
        for report in reports
    )


def day_02b_one_line(reports: list[list[int]]) -> int:
    return sum(
        (
            all(
                level1 - level2 in (1, 2, 3)
                for level1, level2 in zip(report[:-1], report[1:])
            )
            or all(
                level1 - level2 in (-1, -2, -3)
                for level1, level2 in zip(report[:-1], report[1:])
            )
        )
        or any(
            (
                all(
                    level1 - level2 in (1, 2, 3)
                    for level1, level2 in zip(modified_report[:-1], modified_report[1:])
                )
                or all(
                    level1 - level2 in (-1, -2, -3)
                    for level1, level2 in zip(modified_report[:-1], modified_report[1:])
                )
            )
            for modified_report in [
                [level for i, level in enumerate(report) if i != remove]
                for remove in range(len(report))
            ]
        )
        for report in reports
    )


if __name__ == "__main__":
    day_02_input = get_day_02_input()
    answer_02a = day_02a(day_02_input)
    print(answer_02a)
    answer_02b = day_02b(day_02_input)
    print(answer_02b)
