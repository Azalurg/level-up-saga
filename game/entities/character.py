import math
from random import random
from typing import Tuple

import pygame
from pygame import Rect

from game.config import GRID_SIZE


class BaseCharacter:
    id: int
    hp: int
    max_hp: int
    attack: int
    range: int
    cooldown: int
    base_cooldown: int
    color: Tuple[int, int, int]
    rect: Rect
    targets_distance: dict
    in_range: list
    speed: int

    def __init__(self, x, y, color):
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.range = 0.5 * GRID_SIZE
        self.cooldown = 0
        self.base_cooldown = 1
        self.color = color
        self.speed = 200
        self.targets_distance = {}
        self.in_range = []
        self.size = 7

        self.id = hash(f"{x}{y}{random()}")

        self.rect = Rect(
            x * GRID_SIZE + self.size / 2,
            y * GRID_SIZE + self.size / 2,
            GRID_SIZE - self.size,
            GRID_SIZE - self.size,
        )

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

        # Health bar
        health_width = (self.rect.width - 4) * (self.hp / self.max_hp)
        pygame.draw.rect(
            surface,
            (150, 30, 60),
            (self.rect.x + 2, self.rect.y - 15, self.rect.width - 4, 8),
        )
        pygame.draw.rect(
            surface, (50, 150, 50), (self.rect.x + 2, self.rect.y - 15, health_width, 8)
        )

    def calculate_distance(self, targets):
        self.in_range = []
        self.targets_distance = {}

        for target in targets:
            dx = target.rect.centerx - self.rect.centerx
            dy = target.rect.centery - self.rect.centery
            distance = math.hypot(abs(dx), abs(dy))
            if distance <= self.range:
                self.in_range.append(target)
            self.targets_distance[distance] = (dx, dy)

    def select_target(self):
        target = None
        if self.in_range:
            target = min(self.in_range, key=lambda a: a.hp)

        return target

    def update(self, delta_time, targets):
        if self.hp <= 0:
            return

        if not targets:
            return

        if self.cooldown > 0:
            self.cooldown -= delta_time

        self.calculate_distance(targets)

        target = self.select_target()

        if target and self.cooldown <= 0:
            target.hp -= self.attack
            self.cooldown = self.base_cooldown
        if not target:
            # Move towards closest ally
            if targets:
                distance = min(self.targets_distance)
                dx, dy = self.targets_distance[distance]
                if distance > 0:
                    self.rect.x += dx / distance * self.speed * delta_time
                    self.rect.y += dy / distance * self.speed * delta_time
