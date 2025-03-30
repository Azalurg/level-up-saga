import math
from random import random
from typing import Tuple

import pygame

from game.config import GRID_SIZE, HEALTH_BAR_HEIGHT, HEALTH_BAR_GAP
from game.ui.shapes.base import BaseShape
from game.ui.shapes.square import Square


class BaseCharacter:
    id: int
    hp: int
    max_hp: int
    attack: int
    range: int
    cooldown: int
    base_cooldown: int
    color: Tuple[int, int, int]
    shape: BaseShape
    targets_distance: dict
    in_range: list
    speed: int

    def __init__(self, x, y, color, scale=0.65):
        self.id = hash(f"{x}{y}{random()}")
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.range = 1 * GRID_SIZE
        self.cooldown = 0
        self.base_cooldown = 1
        self.color = color
        self.speed = 200
        self.targets_distance = {}
        self.in_range = []
        self.scale = scale

        self.shape = Square(x, y, color, self.scale)  # TODO: Move to separate method

    def _draw_health_bar(self, surface):
        max_health_width = int(self.shape.width * 0.81)
        health_width = max_health_width * (self.hp / self.max_hp)
        health_x = self.shape.centerx - int(self.shape.halfwidth * 0.81)
        health_y = (
            self.shape.centery
            - self.shape.halfheight
            - HEALTH_BAR_HEIGHT
            - HEALTH_BAR_GAP
        )
        pygame.draw.rect(
            surface,
            (150, 30, 60),
            (
                health_x,
                health_y,
                max_health_width,
                HEALTH_BAR_HEIGHT,
            ),
        )
        pygame.draw.rect(
            surface,
            (50, 150, 50),
            (health_x, health_y, health_width, HEALTH_BAR_HEIGHT),
        )

    def draw(self, surface):
        self.shape.draw(surface)
        self._draw_health_bar(surface)

    def calculate_distance(self, targets):
        self.in_range = []
        self.targets_distance = {}

        for target in targets:
            dx = target.shape.centerx - self.shape.centerx
            dy = target.shape.centery - self.shape.centery
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
                    self.shape.centerx += dx / distance * self.speed * delta_time
                    self.shape.centery += dy / distance * self.speed * delta_time
