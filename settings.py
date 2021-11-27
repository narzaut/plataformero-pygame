import pygame as pg
# game options/settings
TITLE = "Jumpy!"
WIDTH = 1366
HEIGHT = 768
FPS = 60
SPACING = 70
# player hitbox rect
PLAYER_HIT_RECT = pg.Rect(0, 0, 50, 70)

# player properties
PLAYER_ACC = 1
PLAYER_FRICTION = 0.13
PLAYER_DASH_SPEED = 30
PLAYER_JUMP_SPEED = 13
# tilesize
TILESIZE = 16

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)