import sys

from random import shuffle
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

        self.generate_boxes()
        # while not (self.check_sum(self.rows) and self.check_sum(self.columns)):
        #    self.generate_boxes()

        if drawing_mode.lower() == "utf8":
            self.spacers = [" │ ", "─", "┼"]
        elif drawing_mode.lower() == "ascii":
            self.spacers = [" | ", "-", "+"]
        else:
            self.spacers = ["  ", " ", " "]

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
            box_row.append(Box(self.complexity, self.digits))
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
    def __init__(self, complexity: int, digits: List[Digit]):
        size = complexity ** 2
        self.digits = digits[0:size]
        shuffle(self.digits)
        self.sequence: List[List[Digit]] = []
        subsequence = []
        for i, digit in enumerate(self.digits):
            subsequence.append(digit)
            if (i + 1) % complexity == 0:
                self.sequence.append(subsequence)
                subsequence = []

    def __str__(self):
        return "\n".join(
            "".join([d.symbol for d in subseq]) for subseq in self.sequence
        )


class Line:
    def __init__(self):
        self.digits = []


class Row(Line):
    pass


class Column(Line):
    pass


p = Puzzle(3)
sys.stdout.write(str(p) + "\n\n")
