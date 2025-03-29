import random
from enum import EnumMeta
from typing import List

import pygame

from game.config import ENEMY_AREA, COLORS, WIDTH, GRID_SIZE, HEIGHT, PLAYER_AREA
from game.entities.character import BaseCharacter


class GameState(EnumMeta):
    SETUP = "SETUP"
    BATTLE = "BATTLE"
    LOST = "LOST"
    VICTORY = "VICTORY"


# class Game:
#     def __init__(self):
#         self.state = GameState.SETUP
#         self.allies = []
#         self.enemies = []
#         self.screen_size = (890, 550)

# def run(self):
#     # Główna pętla gry
#     pygame.init()
#     screen = pygame.display.set_mode(self.screen_size)
#     clock = pygame.time.Clock()
#
#     while True:
#         dt = clock.tick(60) / 1000.0
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 break
#
#         # Logika gry
#         # for ally in self.allies:
#         #     ally.update()
#         # for enemy in self.enemies:
#         #     enemy.update()
#
#         for ally in self.allies:
#             ally.draw(screen)
#         for enemy in self.enemies:
#             enemy.draw(screen)
#
#         # Rysowanie
#         screen.fill((30, 30, 30))
#         for ally in self.allies:
#             ally.draw(screen)
#         for enemy in self.enemies:
#             enemy.draw(screen)
#
#         pygame.display.flip()
#
#     pygame.quit()


class Game:
    def __init__(self, wave=0):
        self.state = GameState.SETUP
        self.wave = wave
        self.allies: List[BaseCharacter] = []
        self.enemies: List[BaseCharacter] = []
        self.selected_unit = None
        self.result_text = ""

    def spawn_wave(self):
        self.wave += 1
        num_enemies = 3 + self.wave
        for _ in range(num_enemies):
            x = random.randint(ENEMY_AREA[0], ENEMY_AREA[0] + ENEMY_AREA[2] - 1)
            y = random.randint(ENEMY_AREA[1], ENEMY_AREA[1] + ENEMY_AREA[3] - 1)
            self.enemies.append(BaseCharacter(x, y, COLORS["enemy"]))

    def check_victory(self):
        if not self.enemies:
            self.result_text = "VICTORY!"
            self.state = GameState.VICTORY
        elif not self.allies:
            self.result_text = "DEFEAT!"
            self.state = GameState.LOST

    def run(self):
        pygame.init()
        font = pygame.font.Font(None, 74)
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        dragging = False

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

                    # Sprawdź, czy miejsce należy do strefy gracza
                    if PLAYER_AREA[0] <= grid_x < PLAYER_AREA[0] + PLAYER_AREA[2]:
                        if PLAYER_AREA[1] <= grid_y < PLAYER_AREA[1] + PLAYER_AREA[3]:
                            self.selected_unit = BaseCharacter(
                                grid_x, grid_y, COLORS["ally"]
                            )
                            self.selected_unit.attack += self.wave
                            self.selected_unit.rect.center = pos
                            dragging = True

                elif event.type == pygame.MOUSEMOTION and dragging:
                    self.selected_unit.rect.center = event.pos

                elif event.type == pygame.MOUSEBUTTONUP and dragging:
                    # Sprawdź prawidłową pozycję
                    grid_x = self.selected_unit.rect.x // GRID_SIZE
                    grid_y = self.selected_unit.rect.y // GRID_SIZE

                    if (
                        PLAYER_AREA[0] <= grid_x < PLAYER_AREA[0] + PLAYER_AREA[2]
                        and PLAYER_AREA[1] <= grid_y < PLAYER_AREA[1] + PLAYER_AREA[3]
                    ):
                        self.allies.append(self.selected_unit)
                    else:
                        # Nieprawidłowa pozycja - anuluj
                        pass

                    self.selected_unit = None
                    dragging = False

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
                    elif event.key == pygame.K_c and self.state == GameState.VICTORY:
                        self.__init__(self.wave)
                        continue

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
            if self.state == GameState.SETUP:
                text = font.render(
                    f"WAVE {self.wave + 1} - PRESS SPACE TO START", True, COLORS["text"]
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
                    text = font.render("PRESS C TO CONTINUE", True, COLORS["text"])
                    screen.blit(
                        text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 100)
                    )

            pygame.display.flip()
