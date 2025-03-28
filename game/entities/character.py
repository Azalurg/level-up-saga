from typing import Tuple

import pygame
from pygame import Rect

from game.config import GRID_SIZE

class CharacterBase:
    id: str
    hp: int
    max_hp: int
    attack: int
    range: int
    cooldown: int
    color: Tuple[int, int, int]
    # team: str
    shape: Rect

    def __init__(self, x, y, color):
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.range = 5
        self.cooldown = 0
        self.color = color

        self.shape = Rect(x*GRID_SIZE + 1, y*GRID_SIZE + 1, GRID_SIZE - 2, GRID_SIZE - 2)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.shape)

        # Health bar
        health_width = (self.shape.width - 4) * (self.hp / self.max_hp)
        pygame.draw.rect(surface, (150, 30, 30), (self.shape.x + 2, self.shape.y - 15, self.shape.width - 4, 8))
        pygame.draw.rect(surface, (50, 150, 50), (self.shape.x + 2, self.shape.y - 15, health_width, 8))
