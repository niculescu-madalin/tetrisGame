import sys
import random
import pygame
from pygame.locals import *
import colors

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

GRID_COLS = 10
GRID_ROWS = 20
BLOCK_SIZE = 32
BLOCK_GAP = 3
PLAY_WIDTH = BLOCK_SIZE * GRID_COLS
PLAY_HEIGHT = BLOCK_SIZE * GRID_ROWS
PLAY_OFFSET_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
PLAY_OFFSET_Y = (SCREEN_HEIGHT - PLAY_HEIGHT) // 2


# Shapes and their rotations
SHAPES = [
    {  # I
        'rotations': [
            [(-1, 0), (0, 0), (1, 0), (2, 0)],
            [(0, -1), (0, 0), (0, 1), (0, 2)]
        ],
        'color': colors.CYAN
    },
    {  # O
        'rotations': [
            [(0, 0), (1, 0), (0, 1), (1, 1)]
        ],
        'color': colors.YELLOW
    },
    {  # T
        'rotations': [
            [(-1, 0), (0, 0), (1, 0), (0, 1)],
            [(0, -1), (0, 0), (0, 1), (-1, 0)],
            [(-1, 0), (0, 0), (1, 0), (0, -1)],
            [(0, -1), (0, 0), (0, 1), (1, 0)]
        ],
        'color': colors.PURPLE
    },
    {  # L
        'rotations': [
            [(-1, 0), (0, 0), (1, 0), (1, 1)],
            [(0, -1), (0, 0), (0, 1), (1, -1)],
            [(-1, -1), (-1, 0), (0, 0), (1, 0)],
            [(-1, 1), (0, -1), (0, 0), (0, 1)]
        ],
        'color': colors.ORANGE
    },
    {  # J
        'rotations': [
            [(-1, 0), (0, 0), (1, 0), (-1, 1)],
            [(0, -1), (0, 0), (0, 1), (1, 1)],
            [(1, -1), (-1, 0), (0, 0), (1, 0)],
            [(-1, -1), (0, -1), (0, 0), (0, 1)]
        ],
        'color': colors.BLUE
    },
    {  # S
        'rotations': [
            [(-1, 0), (0, 0), (0, 1), (1, 1)],
            [(0, -1), (0, 0), (-1, 0), (-1, 1)]
        ],
        'color': colors.GREEN
    },
    {  # Z
        'rotations': [
            [(-1, 1), (0, 1), (0, 0), (1, 0)],
            [(0, -1), (0, 0), (1, 0), (1, 1)]
        ],
        'color': colors.RED
    }
]

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Tetris")


def drawGrid():
    pygame.draw.rect(screen, colors.BEAVER_300, (
        PLAY_OFFSET_X,
        PLAY_OFFSET_Y,
        PLAY_WIDTH + BLOCK_GAP,
        PLAY_HEIGHT + BLOCK_GAP
    ))
    for x in range(GRID_ROWS):
        for y in range(GRID_COLS):
            pygame.draw.rect(screen, colors.BEAVER_800, (
                PLAY_OFFSET_X + BLOCK_GAP + y * BLOCK_SIZE,
                PLAY_OFFSET_Y + BLOCK_GAP + x * BLOCK_SIZE,
                BLOCK_SIZE - BLOCK_GAP,
                BLOCK_SIZE - BLOCK_GAP
            ))

def drawPieces():
    pygame.draw.rect(screen, colors.YELLOW, (
        PLAY_OFFSET_X + BLOCK_GAP,
        PLAY_OFFSET_Y + BLOCK_GAP,
        BLOCK_SIZE - BLOCK_GAP,
        BLOCK_SIZE - BLOCK_GAP
    ))


running = True
while running:
    screen.fill(colors.BLACK)
    drawGrid()
    drawPieces()

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
