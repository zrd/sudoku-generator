import sys

from typing import List

from digit import Digit
from symbols import SYMBOLS


class Puzzle:
    def __init__(self, complexity: int = 3, drawing_mode: str = "utf8"):
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

    def generate_boxes(self):
        boxes = []
        box_row = []
        for i in range(self.size):
            box_row.append(Box(self.complexity, self.null_digit))
            if (i + 1) % self.complexity == 0:
                boxes.append(box_row)
                box_row = []

        self.boxes = boxes
        self.rows = self.populate_rows()
        self.columns = self.populate_columns()

    def populate_rows(self) -> List[List[Digit]]:
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

    def populate_columns(self) -> List[List[Digit]]:
        columns = [[] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                columns[i].append(self.rows[j][i])

        return columns


class Box:
    def __init__(self, complexity: int, null_digit: Digit):
        self.complexity = complexity
        self.null_digit = null_digit
        self.sequence: List[List[Digit]] = [
            [self.null_digit] * self.complexity for _ in range(self.complexity)
        ]

    def __str__(self):
        return "\n".join(
            ["".join([str(d) for d in subseq]) for subseq in self.sequence]
        )

    def insert(self, digit: Digit, col: int, row: int):
        if col + 1 > self.complexity or row + 1 > self.complexity or col < 0 or row < 0:
            raise ValueError(
                "Invalid row, column for {0}x{0} box: ({1},{2})".format(
                    str(self.complexity), str(col), str(row)
                )
            )
        self.sequence[row][col] = digit

    def delete(self, col: int, row: int):
        if col + 1 > self.complexity or row + 1 > self.complexity or col < 0 or row < 0:
            raise ValueError(
                "Invalid row, column for {0}x{0} box: ({1},{2})".format(
                    str(self.complexity), str(col), str(row)
                )
            )
        self.sequence[row][col] = self.null_digit


class Line:
    def __init__(self):
        self.digits = []


class Row(Line):
    pass


class Column(Line):
    pass


p = Puzzle(3)
sys.stdout.write(str(p) + "\n\n")
