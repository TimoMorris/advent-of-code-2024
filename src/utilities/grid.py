"""Class for a general-purpose grid structure with cells.

Methods supporting finding neighbouring cells and getting all cells in the grid matching certain criteria.
"""

from typing import Self, Type, TypeAlias, Iterable, Callable, Literal, TypeVar

Coordinates: TypeAlias = tuple[int, int]
SearchStrategy: TypeAlias = Literal["adjacent", "diagonal", "neighbouring"]
CellFilter: TypeAlias = Callable[["Cell"], bool]
TValue = TypeVar("TValue", bound=int | str)

STRAIGHT_VECTORS: list[Coordinates] = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # clockwise from east
DIAGONAL_VECTORS: list[Coordinates] = [(1, 1), (1, -1), (-1, -1), (-1, 1)]  # clockwise from southeast
ALL_VECTORS: list[Coordinates] = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]  # clockwise from east


class Cell[TValue]:
    """A single element within a grid."""
    def __init__(self, row: int, col: int, value: TValue, *, grid=None):
        self.row: int = row
        self.col: int = col
        self.value: TValue = value
        self._grid: "Grid" = grid

    def __add__(self, other: Coordinates) -> Self:
        row_offset, col_offset = other
        return self._grid.try_get_cell(self.row + row_offset, self.col + col_offset)

    def _get_offsetted_cells(self, offsets: list[Coordinates]) -> Iterable[Self]:
        for offset in offsets:
            if (offset_cell := self + offset) is not None:
                yield offset_cell

    def get_adjacent_cells(self) -> Iterable[Self]:
        return self._get_offsetted_cells(STRAIGHT_VECTORS)

    def get_diagonal_cells(self) -> Iterable[Self]:
        return self._get_offsetted_cells(DIAGONAL_VECTORS)

    def get_neighboring_cells(self) -> Iterable[Self]:
        return self._get_offsetted_cells(ALL_VECTORS)


TCell = TypeVar("TCell", bound=Cell)

class Grid[TCell]:
    """A grid of cells."""
    def __init__(self, height: int, width: int):
        self.height: int = height
        self.width: int = width
        self._rows: list[list[TCell]] = [[] for __ in range(self.height)]
        self._cols: list[list[TCell]] = [[] for __ in range(self.width)]
        self._cells: dict[Coordinates, TCell] = {}

    @classmethod
    def from_lists(cls, lists: Iterable[Iterable[int | str]], cell_class: Type[TCell] = Cell) -> "Grid":  # return type should be Self but bug in PyCharm
        """Create a grid from a list of lists"""
        lists = [[x for x in list_] for list_ in lists]
        grid = cls(len(lists), len(lists[0]))
        for row, list_ in enumerate(lists):
            for col, item in enumerate(list_):
                cell = cell_class(row, col, item, grid=grid)
                grid._cells[row, col] = cell
                grid._rows[row].append(cell)
                grid._cols[col].append(cell)

        assert len(grid._cells) == grid.height * grid.width
        assert all(len(row) == grid.width for row in grid._rows)
        assert all(len(col) == grid.height for col in grid._cols)

        return grid

    @classmethod
    def from_strings(cls, strings: Iterable[str], cell_class: Type[TCell] = Cell) -> "Grid":  # return type should be Self but bug in PyCharm
        """Create a grid from a list of strings."""
        return cls.from_lists(strings, cell_class=cell_class)

    def try_get_cell(self, row, col):
        """Fetch the cell at the given row and column if it exists."""
        if 0 <= row < self.height and 0 <= col < self.width:
            return self._cells[(row, col)]

    def get_cells(self, condition: Callable[[TCell], bool]) -> Iterable[TCell]:
        """Get all cells in the grid matching the given condition."""
        for cell in self._cells.values():
            if condition(cell):
                yield cell

    @staticmethod
    def connect_cells(
        starting_cells: list[TCell],
        can_connect: Callable[[TCell, TCell], bool],
        connect: Callable[[TCell, TCell], None],
        # *,
        # search: SearchStrategy = "adjacent"
    ) -> None:
        """Recursively loop over neighbouring cells, connecting those matching the condition.

        Perform breadth-first search over neighbouring cells and connect any that match the condition.
        Add these to the set to search from in the next iteration.
        The search will terminate when the current iteration adds no cells to search in the next iteration.

        Cells can be considered multiple times, including potentially in different search iterations,
        and there is no mechanism to ensure the search terminates,
        so this must emerge as a consequence of the `can_connect` condition.

        Args:
            `starting_cells`: the initial cells from which to search for connections
            `can_connect`: callable taking a candidate cell and its parent cell (respectively),
                and returning whether the candidate cell can be connected to the parent
            `connect`: callable taking a candidate cell and its parent cell (respectively),
                and performing the action to connect them (whatever this entails in the given scenario)

        """
        current_generation: set[TCell] = set(starting_cells)
        next_generation: set[TCell] = set()

        while current_generation:
            cell = current_generation.pop()
            for adj_cell in cell.get_adjacent_cells():
                if can_connect(adj_cell, cell):
                    connect(adj_cell, cell)
                    next_generation.add(adj_cell)

            if not current_generation and next_generation:
                current_generation = next_generation
                next_generation = set()
