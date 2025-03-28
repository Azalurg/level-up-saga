from typing import Tuple


class Character:
    position: Tuple[int, int]
    destination: Tuple[int, int]
    name: chr

    def __init__(
        self, position: Tuple[int, int], destination: Tuple[int, int], name: chr
    ):
        self.position = position
        self.destination = destination
        self.name = name

    def move(self):
        x_diff = abs(self.destination[0] - self.position[0])
        y_diff = abs(self.destination[1] - self.position[1])
        if x_diff > y_diff:
            if self.destination[0] > self.position[0]:
                self.position = (self.position[0] + 1, self.position[1])
            else:
                self.position = (self.position[0] - 1, self.position[1])
        else:
            if self.destination[1] > self.position[1]:
                self.position = (self.position[0], self.position[1] + 1)
            else:
                self.position = (self.position[0], self.position[1] - 1)

    def x(self) -> int:
        return self.position[0]

    def y(self) -> int:
        return self.position[1]
