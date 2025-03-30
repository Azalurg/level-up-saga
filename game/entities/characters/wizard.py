from game.config import GRID_SIZE
from game.entities.character import BaseCharacter
from game.ui.shapes.hex import Hex


class Wizard(BaseCharacter):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.hp = 20
        self.max_hp = 20
        self.attack = 50
        self.range = 5 * GRID_SIZE
        self.cooldown = 0
        self.base_cooldown = 3

        self.shape = Hex(x, y, color, self.scale)
