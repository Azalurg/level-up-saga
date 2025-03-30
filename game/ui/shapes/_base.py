from typing import Tuple

from game.config import GRID_SIZE


class BaseShape:
    grid_x: int
    grid_y: int
    grid_scale: float
    color: Tuple[int, int, int]

    centerx: int
    centery: int
    width: int
    height: int
    halfwidth: int
    halfheight: int
    topleft: Tuple[int, int]
    topright: Tuple[int, int]

    def __init__(self, grid_x, grid_y, color, size: float):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.color = color

        if size <= 0:
            raise ValueError("Size must be greater than 0")

        self.size = size
        self.width = GRID_SIZE * size
        self.height = GRID_SIZE * size
        self.halfwidth = self.width // 2
        self.halfheight = self.height // 2
        self.centerx = self.grid_x * GRID_SIZE + GRID_SIZE // 2
        self.centery = self.grid_y * GRID_SIZE + GRID_SIZE // 2
        self.topleft = (self.grid_x * GRID_SIZE, self.grid_y * GRID_SIZE)
        self.topright = (self.grid_x * GRID_SIZE + self.width, self.grid_y * GRID_SIZE)

    def draw(self, screen):
        raise NotImplementedError

    def __str__(self):
        return f"{self.__class__.__name__}({self.grid_x}, {self.grid_y}, {self.color}, {self.width}, {self.height}, {self.centerx}, {self.centery}, {self.topleft}, {self.topright})"
