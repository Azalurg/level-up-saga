from enum import EnumMeta

import pygame


class GameState(EnumMeta):
    SETUP = 'SETUP'


class Game:
    def __init__(self):
        self.state = GameState.SETUP
        self.allies = []
        self.enemies = []
        self.screen_size = (890, 550)

    def run(self):
        # Główna pętla gry
        pygame.init()
        screen = pygame.display.set_mode(self.screen_size)
        clock = pygame.time.Clock()

        while True:
            dt = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

            # Logika gry
            # for ally in self.allies:
            #     ally.update()
            # for enemy in self.enemies:
            #     enemy.update()

            for ally in self.allies:
                ally.draw(screen)
            for enemy in self.enemies:
                enemy.draw(screen)

            # Rysowanie
            screen.fill((30, 30, 30))
            for ally in self.allies:
                ally.draw(screen)
            for enemy in self.enemies:
                enemy.draw(screen)

            pygame.display.flip()

        pygame.quit()
