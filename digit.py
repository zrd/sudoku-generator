from dataclasses import dataclass


@dataclass(eq=True, order=True)
class Digit:
    symbol: str
    value: int
