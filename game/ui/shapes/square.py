import pygame

from game.config import GRID_SIZE
from game.ui.shapes._base import BaseShape


class Square(BaseShape):
    def __init__(self, grid_x, grid_y, color, size=0.80):
        super().__init__(grid_x, grid_y, color, size)

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            (
                self.centerx - self.halfwidth,
                self.centery - self.halfheight,
                self.width,
                self.height,
            ),
        )
