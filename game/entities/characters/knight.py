import pygame.draw
from numpy.ma.core import shape

from game.config import GRID_SIZE
from game.entities.character import BaseCharacter


class Knight(BaseCharacter):

    def __init__(self, x, y, color):
        super().__init__(x, y, color, 0.9)
        self.hp = 200
        self.max_hp = 200
        self.attack = 15
        self.range = 0.5 * GRID_SIZE
        self.cooldown = 0
        self.base_cooldown = 2
        self.speed = 160
