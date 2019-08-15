from __future__ import annotations

import random
import sys

from typing import List, Tuple, Union

from digit import Digit
from symbols import SYMBOLS


class Puzzle:
    def __init__(self, complexity: int = 3, drawing_mode: str = "utf8") -> None:
        self.size = complexity ** 2
        self.digits = []
        for i, symbol in enumerate(SYMBOLS):
            if i < self.size:
                self.digits.append(Digit(symbol, i + 1))
            else:
                break

        self.digits.sort()
        max_complexity = int(len(SYMBOLS) ** (1 / 2))
        if complexity < 1 or complexity > max_complexity:
            raise ValueError(
                "Puzzle complexity: expected integer from 1 to {}. Got {}".format(
                    str(max_complexity), str(complexity)
                )
            )
        else:
            self.complexity = complexity

        if drawing_mode.lower() == "utf8":
            self.null_digit = Digit("·", 0)
            self.spacers = [" │ ", "─", "┼"]
        elif drawing_mode.lower() == "ascii":
            self.null_digit = Digit(" ", 0)
            self.spacers = [" | ", "-", "+"]
        else:
            self.null_digit = Digit("0", 0)
            self.spacers = ["  ", " ", " "]

        self.generate_boxes()
        # while not (self.check_sum(self.rows) and self.check_sum(self.columns)):
        #    self.generate_boxes()
        self.fill_random_square()

    def __str__(self):
        rows = []
        pretty_row = []
        vertical_spacer, horizontal_spacer, juncture = self.spacers
        unit_width = (
            self.complexity + len(vertical_spacer)
            if len(vertical_spacer) > 1
            else self.complexity + 1
        )
        for i, row in enumerate(self.rows):
            for j, digit in enumerate(row):
                if j > 0 and j % self.complexity == 0:
                    pretty_row.append(vertical_spacer)
                pretty_row.append(digit.symbol)

            rows.append(pretty_row)
            pretty_len = sum([len(d) for d in pretty_row])
            adjustment = len(vertical_spacer) - int(len(vertical_spacer) / 2) or 1
            pretty_row = []
            spacer_line = []
            if (i + 1) < self.size and (i + 1) % self.complexity == 0:
                for k in range(pretty_len):
                    if (k + adjustment) % unit_width == 0:
                        spacer_line.append(juncture)
                    else:
                        spacer_line.append(horizontal_spacer)

                rows.append(spacer_line)

        return "\n".join(["".join(row) for row in rows])

    def digit(self, row: int, col: int) -> Digit:
        return self.rows[row][col]

    def box(self, row: int, col: int) -> Box:
        box_row = int(row / self.complexity)
        box_col = col % self.complexity
        return self.boxes[box_row][box_col]

    def box_coordinates(self, row: int, col: int) -> Tuple[int, int]:
        return self.complexity, self.complexity

    def insert(self, digit, row, col):
        # Whole puzzle coordinates -> Box + box coordinates
        self.update_lines()

    def delete(self, row, col):
        # Whole puzzle coordinates -> Box + box coordinates
        self.update_lines()

    def legal_digit(self, digit, row, col):
        return True

    def fill_random_square(self, digit: Union[None, Digit] = None):
        if digit is None:
            digit = self.digits[random.choice(range(self.size))]

        filled = False
        while not filled:
            row = random.choice(range(self.size))
            col = random.choice(range(self.size))
            if not self.digit(row, col).value:
                if self.legal_digit(digit, row, col):
                    self.insert(digit, row, col)
                    filled = True

    def generate_boxes(self):
        boxes = []
        box_row = []
        for i in range(self.size):
            box_row.append(Box(self.complexity, self.null_digit))
            if (i + 1) % self.complexity == 0:
                boxes.append(box_row)
                box_row = []

        self.boxes = boxes
        self.update_lines()


    def _populate_rows(self) -> List[List[Digit]]:
        rows = []
        row = []
        for box_row in self.boxes:
            for i in range(self.complexity):
                for j, box in enumerate(box_row):
                    row += box.sequence[i]
                    if (j + 1) % self.complexity == 0:
                        rows.append(row)
                        row = []

        return rows

    def _populate_columns(self) -> List[List[Digit]]:
        columns = [[] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                columns[i].append(self.rows[j][i])

        return columns

    def update_lines(self) -> None:
        self.rows = self._populate_rows()
        self.columns = self._populate_columns()


class Box:
    def __init__(self, complexity: int, null_digit: Digit) -> None:
        self.complexity = complexity
        self.null_digit = null_digit
        self.sequence: List[List[Digit]] = [
            [self.null_digit] * self.complexity for _ in range(self.complexity)
        ]

    def __str__(self):
        return "\n".join(
            ["".join([str(d) for d in subseq]) for subseq in self.sequence]
        )

    def digits(self):
        return [d for row in self.sequence for d in row]

    def insert(self, digit: Digit, row: int, col: int):
        if col + 1 > self.complexity or row + 1 > self.complexity or col < 0 or row < 0:
            raise ValueError(
                "Invalid row, column for {0}x{0} box: ({1},{2})".format(
                    str(self.complexity), str(row), str(col)
                )
            )
        self.sequence[row][col] = digit

    def delete(self, row: int, col: int):
        self.insert(self.null_digit, row, col)


for sz in range(1, 7):
    for dm in ("utf8", "ascii", "whitespace"):
        p = Puzzle(sz, drawing_mode=dm)
        sys.stdout.write(str(p) + "\n\n")
