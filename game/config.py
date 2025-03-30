GRID_SIZE = 42
WIDTH_P, HEIGHT_P = 30, 20
WIDTH, HEIGHT = GRID_SIZE * WIDTH_P, GRID_SIZE * HEIGHT_P
PLAYER_AREA = (1, 1, 6, 11)
ENEMY_AREA = (WIDTH_P - 7, 1, 6, 11)

COLORS = {
    "background": (30, 30, 40),
    "grid": (60, 60, 80),
    "player_zone": (60, 120, 60),
    "enemy_zone": (120, 60, 60),
    "ally": (20, 200, 120),
    "enemy": (200, 80, 20),
    "text": (200, 200, 0),
}
