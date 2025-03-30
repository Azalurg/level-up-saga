import pygame.draw
from numpy.ma.core import shape

from game.config import GRID_SIZE
from game.entities.character import BaseCharacter
from game.ui.shapes.triangle import Triangle


class Archer(BaseCharacter):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.hp = 20
        self.max_hp = 20
        self.attack = 20
        self.range = 3 * GRID_SIZE
        self.cooldown = 0
        self.base_cooldown = 1

        self.shape = Triangle(x, y, color, self.scale)
