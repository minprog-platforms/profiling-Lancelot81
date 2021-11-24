from __future__ import annotations
from typing import Iterable


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        self._grid: list[str] = []

        for puzzle_row in puzzle:
            row = ""

            for element in puzzle_row:
                row += str(element)

            self._grid.append(row)

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        self._grid[y] = self._grid[y][:x] + str(value) + self._grid[y][x+1:]

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        self._grid[y] = self._grid[y][:x] + "0" + self._grid[y][x+1:]

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        return int(self._grid[y][x])

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""
        options = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        options = options - set(self.row_values(y))
        options = options - set(self.column_values(x))
        options = options - set(self.block_values((y // 3) * 3 + x // 3))

        return options

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        for y in range(9):
            for x in range(9):
                if self._grid[y][x] == '0':
                    return x, y

        return -1, -1

    def row_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th row."""
        return map(int, self._grid[i])

    def column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""
        return [int(row[i]) for row in self._grid]

    def block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """

        x_start = (i % 3) * 3
        y_start = (i // 3) * 3

        values1 = list(map(int, self._grid[y_start][x_start:x_start+3]))
        values2 = list(map(int, self._grid[y_start+1][x_start:x_start+3]))
        values3 = list(map(int, self._grid[y_start+2][x_start:x_start+3]))
        values = values1 + values2 + values3

        return values

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        if any('0' in row for row in self._grid):
            return False

        all = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        if any(set(self.row_values(i)) != all for i in range(9)):
            return False

        if any(set(self.column_values(i)) != all for i in range(9)):
            return False

        if any(set(self.block_values(i)) != all for i in range(9)):
            return False


        return True


    def __str__(self) -> str:
        representation = ""

        for row in self._grid:
            representation += row + "\n"

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[str] = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")

            puzzle.append(line)

    return Sudoku(puzzle)
