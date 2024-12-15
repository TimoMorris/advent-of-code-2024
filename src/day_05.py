from collections import defaultdict
from dataclasses import dataclass
from functools import total_ordering


def get_day_05_input() -> tuple[list[tuple[int, int]], list[list[int]]]:
    with open("inputs/input_05.txt") as f:
        contents = f.read().splitlines()

    empty_line_no = contents.index("")
    ordering_rules_as_str = [c.split("|") for c in contents[:empty_line_no]]
    updates_as_str = [c.split(",") for c in contents[empty_line_no + 1:]]

    ordering_rules = [(int(a), int(b)) for a, b in ordering_rules_as_str]
    updates = [[int(x) for x in pages] for pages in updates_as_str]
    return ordering_rules, updates


def is_update_valid(update: list[int], pages_must_occur_after_it: defaultdict[int, set[int]]) -> bool:
    for i, page in enumerate(update):
        pages_before_it = update[:i]
        if set(pages_must_occur_after_it[page]) & set(pages_before_it):
            return False
    else:
        return True


def day_05a(ordering_rules: list[tuple[int, int]], updates: list[list[int]]) -> int:
    pages_must_occur_after_it = defaultdict(set)
    for a, b in ordering_rules:
        pages_must_occur_after_it[a].add(b)

    valid_updates = [update for update in updates if is_update_valid(update, pages_must_occur_after_it)]
    middle_page_sum = sum(update[len(update) // 2] for update in valid_updates)
    return middle_page_sum


@total_ordering
@dataclass
class Page:
    page_no: int
    pages_must_occur_after_it: set[int]

    def __eq__(self, other):
        return self.page_no == other.page_no
    def __lt__(self, other):
        return other.page_no in self.pages_must_occur_after_it
    # Not sure whether page rules guarantee well-defined ordering so adding this to be explicit
    # ie __lt__ is False doesn't mean __gt__ is True... but I'm not sure Python checks both in this case anyway 🤷‍♂️.
    def __gt__(self, other):
        return self.page_no in other.pages_must_occur_after_it


def day_05b(ordering_rules: list[tuple[int, int]], updates: list[list[int]]) -> int:
    pages_must_occur_after_it = defaultdict(set)
    for a, b in ordering_rules:
        pages_must_occur_after_it[a].add(b)

    invalid_updates = [update for update in updates if not is_update_valid(update, pages_must_occur_after_it)]

    corrected_updates = []
    for update in invalid_updates:
        pages = [Page(page_no, set(pages_must_occur_after_it[page_no])) for page_no in update]
        corrected_update = [page.page_no for page in sorted(pages)]  # work happens in the sorted() call
        corrected_updates.append(corrected_update)

    middle_page_sum = sum(update[len(update) // 2] for update in corrected_updates)
    return middle_page_sum


if __name__ == "__main__":
    ordering_rules, updates = get_day_05_input()
    answer_05a = day_05a(ordering_rules, updates)
    print(answer_05a)
    answer_05b = day_05b(ordering_rules, updates)
    print(answer_05b)
