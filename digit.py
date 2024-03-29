from dataclasses import dataclass


@dataclass(eq=True, order=True)
class Digit:
    symbol: str
    value: int

    def __str__(self):
        return self.symbol

    def __bool__(self):
        return bool(self.value)
