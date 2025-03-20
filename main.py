import sys
import random
import pygame
from pygame.locals import *

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

COLS = 10
ROWS = 20
SURFACE_WIDTH = 800
SURFACE_HEIGHT = 700
PLAY_WIDTH = 300
PLAY_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
colorWhite = pygame.Color(255, 255, 255)
colorBlack = pygame.Color(0, 0, 0)

# Tetrimino colors
colorSky = pygame.Color(0, 191, 255)  # I
colorIndigo = pygame.Color(114, 60, 210)  # J
colorOrange = pygame.Color(255, 127, 80)  # L
colorYellow = pygame.Color(255, 215, 0)  # O
colorGreen = pygame.Color(50, 205, 50)  # S
colorPurple = pygame.Color(139, 0, 139)  # T
colorRed = pygame.Color(178, 34, 34)  # Z

# Shapes and their rotations
SHAPES = [
    {  # I
        'rotations': [
            [(-1, 0), (0, 0), (1, 0), (2, 0)],
            [(0, -1), (0, 0), (0, 1), (0, 2)]
        ],
        'color': colorSky
    },
    {  # O
        'rotations': [
            [(0, 0), (1, 0), (0, 1), (1, 1)]
        ],
        'color': colorYellow
    },
    {  # T
        'rotations': [
            [(-1, 0), (0, 0), (1, 0), (0, 1)],
            [(0, -1), (0, 0), (0, 1), (-1, 0)],
            [(-1, 0), (0, 0), (1, 0), (0, -1)],
            [(0, -1), (0, 0), (0, 1), (1, 0)]
        ],
        'color': colorPurple
    },
    {  # L
        'rotations': [
            [(-1, 0), (0, 0), (1, 0), (1, 1)],
            [(0, -1), (0, 0), (0, 1), (1, -1)],
            [(-1, -1), (-1, 0), (0, 0), (1, 0)],
            [(-1, 1), (0, -1), (0, 0), (0, 1)]
        ],
        'color': colorOrange
    },
    {  # J
        'rotations': [
            [(-1, 0), (0, 0), (1, 0), (-1, 1)],
            [(0, -1), (0, 0), (0, 1), (1, 1)],
            [(1, -1), (-1, 0), (0, 0), (1, 0)],
            [(-1, -1), (0, -1), (0, 0), (0, 1)]
        ],
        'color': colorIndigo
    },
    {  # S
        'rotations': [
            [(-1, 0), (0, 0), (0, 1), (1, 1)],
            [(0, -1), (0, 0), (-1, 0), (-1, 1)]
        ],
        'color': colorGreen
    },
    {  # Z
        'rotations': [
            [(-1, 1), (0, 1), (0, 0), (1, 0)],
            [(0, -1), (0, 0), (1, 0), (1, 1)]
        ],
        'color': colorRed
    }
]

surface = pygame.display.set_mode([SURFACE_WIDTH, SURFACE_HEIGHT])
pygame.display.set_caption("Tetris")

# Run until the user asks to quit
running = True
while running:
    surface.fill(colorBlack)
    # Did the user click the window close button?

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Flip the display
    pygame.display.update()

# Done! Time to quit.
pygame.quit()