from collections import Counter


def get_day_01_input() -> tuple[list[int], list[int]]:
    with open("inputs/input_01.txt") as f:
        contents = f.readlines()

    pairs_as_str = [line.strip().split("   ") for line in contents]
    pairs = [(int(a), int(b)) for a, b in pairs_as_str]
    list1, list2 = zip(*pairs)
    return list(list1), list(list2)


def day_01a():
    list1, list2 = get_day_01_input()

    pairs = zip(sorted(list1), sorted(list2))
    distances = [abs(a - b) for a, b in pairs]
    answer = sum(distances)
    return answer


def day_01b():
    list1, list2 = get_day_01_input()

    counts1 = Counter(list1)
    counts2 = Counter(list2)

    totals = [(num, counts2[num]) for num, count in counts1.items()]
    similarity_score = sum(n * c for n, c in totals)
    return similarity_score


if __name__ == "__main__":
    answer_01a = day_01a()
    print(answer_01a)
    answer_01b = day_01b()
    print(answer_01b)
