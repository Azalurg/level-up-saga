import pygame

from game.ui.shapes.base import BaseShape


class Triangle(BaseShape):
    def __init__(self, grid_x, grid_y, color, size=0.80):
        super().__init__(grid_x, grid_y, color, size)

    def draw(self, screen):
        pygame.draw.polygon(
            screen,
            self.color,
            [
                (self.centerx, self.centery - self.halfheight),
                (self.centerx - self.halfwidth, self.centery + self.halfheight),
                (self.centerx + self.halfwidth, self.centery + self.halfheight),
            ],
        )
