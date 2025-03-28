from typing import List
from .character import Character


class Board(object):
    def __init__(self, width, height, field: chr = "."):
        self.width = width
        self.height = height
        self.field = field

    def print(self, characters: List[Character]):
        board = [[self.field] * self.width for _ in range(self.height)]

        for character in characters:
            board[character.x()][character.y()] = character.name

        for row in board:
            print("".join(row))
