import math
from random import random
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
    rect: Rect
    enemies: dict
    speed: int

    def __init__(self, x, y, color):
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.range = 5
        self.cooldown = 0
        self.color = color
        self.speed = 200

        self.id = str(hash(f"{x}{y}{random()}"))

        self.rect = Rect(x*GRID_SIZE + 1, y*GRID_SIZE + 1, GRID_SIZE - 2, GRID_SIZE - 2)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

        # Health bar
        health_width = (self.rect.width - 4) * (self.hp / self.max_hp)
        pygame.draw.rect(surface, (150, 30, 30), (self.rect.x + 2, self.rect.y - 15, self.rect.width - 4, 8))
        pygame.draw.rect(surface, (50, 150, 50), (self.rect.x + 2, self.rect.y - 15, health_width, 8))

    def find_target(self, targets):
        closest = None
        min_dist = float('inf')
        for target in targets:
            if target.hp <= 0:
                continue
            dx = self.rect.centerx - target.rect.centerx
            dy = self.rect.centery - target.rect.centery
            distance = math.hypot(dx, dy)
            if distance < min_dist and distance <= self.range * GRID_SIZE:
                closest = target
                min_dist = distance
        return closest

    def update(self, dt, targets):
        if self.hp <= 0:
            return

        if self.cooldown > 0:
            self.cooldown -= dt

        target = self.find_target(targets)
        if target and self.cooldown <= 0:
            target.hp -= self.attack
            self.cooldown = 1
        if not target:
            # Move towards closest ally
            if targets:
                closest = min(targets, key=lambda a: math.hypot(
                    self.rect.centerx - a.rect.centerx,
                    self.rect.centery - a.rect.centery
                ))
                dx = closest.rect.centerx - self.rect.centerx
                dy = closest.rect.centery - self.rect.centery
                distance = math.hypot(dx, dy)
                if distance > 0:
                    self.rect.x += dx / distance * self.speed * dt
                    self.rect.y += dy / distance * self.speed * dt
