import random
from enum import EnumMeta
from typing import List

import pygame

from game.config import ENEMY_AREA, COLORS, WIDTH, GRID_SIZE, HEIGHT, PLAYER_AREA
from game.entities.character import BaseCharacter
from game.entities.characters.archer import Archer
from game.entities.characters.knight import Knight
from game.entities.characters.wizard import Wizard


class GameState(EnumMeta):
    SETUP = "SETUP"
    BATTLE = "BATTLE"
    LOST = "LOST"
    VICTORY = "VICTORY"


class Game:
    def __init__(self, wave=1, player_grid=None):
        self.state = GameState.SETUP
        self.wave = wave
        self.allies: List[BaseCharacter] = []
        self.enemies: List[BaseCharacter] = []
        self.selected_unit = None
        self.result_text = ""

        self.player_grid = player_grid


        # Part fo the code that will save a player configuration between waves
        if self.player_grid is None:
            self.player_grid = [
                [0 for _ in range(HEIGHT // GRID_SIZE)]
                for _ in range(WIDTH // GRID_SIZE)
            ]

        for x in range(len(self.player_grid)):
            for y in range(len(self.player_grid[x])):
                if self.player_grid[x][y] != 0:
                    to_add_unit = BaseCharacter(
                        x + PLAYER_AREA[0], y + PLAYER_AREA[1], COLORS["ally"]
                    )
                    self.allies.append(to_add_unit)
                    self.player_grid[x][y] = to_add_unit.id

    def spawn_wave(self):
        num_enemies = 3 + self.wave
        for _ in range(num_enemies):
            x = random.randint(ENEMY_AREA[0], ENEMY_AREA[0] + ENEMY_AREA[2] - 1)
            y = random.randint(ENEMY_AREA[1], ENEMY_AREA[1] + ENEMY_AREA[3] - 1)
            r = random.random()
            if r < 0.3:
                self.enemies.append(Knight(x, y, COLORS["enemy"]))
            elif r < 0.6:
                self.enemies.append(Wizard(x, y, COLORS["enemy"]))
            else:
                self.enemies.append(Archer(x, y, COLORS["enemy"]))

    def check_victory(self):
        if not self.enemies:
            self.result_text = "VICTORY!"
            self.state = GameState.VICTORY
            self.wave += 1
        elif not self.allies:
            self.result_text = "DEFEAT!"
            self.state = GameState.LOST

    def run(self):
        pygame.init()
        font = pygame.font.Font(None, 74)
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("LevelUP Saga")
        clock = pygame.time.Clock()

        while True:
            dt = clock.tick(24) / 1000.0
            screen.fill(COLORS["background"])

            # Rysuj siatkę
            for x in range(0, WIDTH, GRID_SIZE):
                pygame.draw.line(screen, COLORS["grid"], (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, GRID_SIZE):
                pygame.draw.line(screen, COLORS["grid"], (0, y), (WIDTH, y))

            # Podświetl strefę gracza
            player_zone_rect = pygame.Rect(
                PLAYER_AREA[0] * GRID_SIZE,
                PLAYER_AREA[1] * GRID_SIZE,
                PLAYER_AREA[2] * GRID_SIZE,
                PLAYER_AREA[3] * GRID_SIZE,
            )
            enemy_zone_rect = pygame.Rect(
                ENEMY_AREA[0] * GRID_SIZE,
                ENEMY_AREA[1] * GRID_SIZE,
                ENEMY_AREA[2] * GRID_SIZE,
                ENEMY_AREA[3] * GRID_SIZE,
            )

            pygame.draw.rect(screen, COLORS["player_zone"], player_zone_rect, 2)
            pygame.draw.rect(screen, COLORS["enemy_zone"], enemy_zone_rect, 2)

            # Obsługa zdarzeń
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                elif (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and self.state == GameState.SETUP
                ):
                    pos = pygame.mouse.get_pos()
                    grid_x = pos[0] // GRID_SIZE
                    grid_y = pos[1] // GRID_SIZE

                    self.selected_unit = BaseCharacter(grid_x, grid_y, COLORS["ally"])
                    self.selected_unit.attack += self.wave

                    if (
                        PLAYER_AREA[0] <= grid_x < PLAYER_AREA[0] + PLAYER_AREA[2]
                        and PLAYER_AREA[1] <= grid_y < PLAYER_AREA[1] + PLAYER_AREA[3]
                        and self.player_grid[grid_x - PLAYER_AREA[0]][
                            grid_y - PLAYER_AREA[1]
                        ]
                        == 0
                    ):
                        self.allies.append(self.selected_unit)
                        self.player_grid[grid_x - PLAYER_AREA[0]][
                            grid_y - PLAYER_AREA[1]
                        ] = self.selected_unit.id

                    elif (
                        self.player_grid[grid_x - PLAYER_AREA[0]][
                            grid_y - PLAYER_AREA[1]
                        ]
                        != 0
                    ):
                        # Usuń jednostkę z listy
                        self.allies = [
                            a
                            for a in self.allies
                            if a.id
                            != self.player_grid[grid_x - PLAYER_AREA[0]][
                                grid_y - PLAYER_AREA[1]
                            ]
                        ]
                        self.player_grid[grid_x - PLAYER_AREA[0]][
                            grid_y - PLAYER_AREA[1]
                        ] = 0
                    else:
                        # Nieprawidłowa pozycja - anuluj
                        print("Invalid position")
                        pass

                    self.selected_unit = None

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.state == GameState.SETUP:
                        self.spawn_wave()
                        self.state = GameState.BATTLE
                    elif event.key == pygame.K_r and self.state in (
                        GameState.LOST,
                        GameState.VICTORY,
                    ):
                        self.__init__()
                        continue
                    elif (
                        event.key == pygame.K_SPACE and self.state == GameState.VICTORY
                    ):
                        self.__init__(self.wave, self.player_grid)
                        continue
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return

            # Logika gry
            if self.state == GameState.BATTLE:
                for ally in self.allies:
                    ally.update(dt, self.enemies)
                for enemy in self.enemies:
                    enemy.update(dt, self.allies)

                # Usuń martwe jednostki
                self.allies = [a for a in self.allies if a.hp > 0]
                self.enemies = [e for e in self.enemies if e.hp > 0]

                self.check_victory()

            # Rysowanie
            for ally in self.allies:
                ally.draw(screen)
            for enemy in self.enemies:
                enemy.draw(screen)

            if self.selected_unit:
                self.selected_unit.draw(screen)

            # Teksty
            ally_count = len(self.allies)
            enemy_count = len(self.enemies)
            text = font.render(
                f"Wave: {self.wave} - Allies: {ally_count} - Enemies: {enemy_count}",
                True,
                COLORS["text"],
            )

            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 10))

            if self.state == GameState.SETUP:
                text = font.render(
                    f"PRESS SPACE TO START", True, COLORS["text"]
                )
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 100))
            elif self.state in (GameState.LOST, GameState.VICTORY):
                text = font.render(self.result_text, True, COLORS["text"])
                screen.blit(
                    text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50)
                )
                text = font.render("PRESS R TO RESTART", True, COLORS["text"])
                screen.blit(
                    text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 50)
                )
                if self.state == GameState.VICTORY:
                    text = font.render("PRESS SPACE TO CONTINUE", True, COLORS["text"])
                    screen.blit(
                        text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 100)
                    )

            pygame.display.flip()
