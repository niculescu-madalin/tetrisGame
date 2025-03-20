import sys
import random
import time
import pygame
from pygame.locals import *
import colors
import shapes

pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

GRID_COLS = 10
GRID_ROWS = 20
BLOCK_SIZE = 32
BLOCK_GAP = 3

PLAY_WIDTH = BLOCK_SIZE * GRID_COLS
PLAY_HEIGHT = BLOCK_SIZE * GRID_ROWS
PLAY_OFFSET_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
PLAY_OFFSET_Y = (SCREEN_HEIGHT - PLAY_HEIGHT) // 2

MOVEMENT_DELAY = 10

# Game state
current_grid_x = 0
current_grid_y = 0

def checkCollision(x, y) -> bool:
    new_x = x + 1
    new_y = y + 1
    if new_x <= 0 or new_x > GRID_COLS or new_y > GRID_ROWS:
        return True
    if new_y <= 0:
        return True
    return False


def move(dx, dy):
    global current_grid_x, current_grid_y
    new_x = current_grid_x + dx
    new_y = current_grid_y + dy
    if not checkCollision(new_x, new_y):
        current_grid_x = new_x
        current_grid_y = new_y



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
        PLAY_OFFSET_X + BLOCK_GAP + current_grid_x * BLOCK_SIZE,
        PLAY_OFFSET_Y + BLOCK_GAP + current_grid_y * BLOCK_SIZE,
        BLOCK_SIZE - BLOCK_GAP,
        BLOCK_SIZE - BLOCK_GAP
    ))


def continue_moving(target_x, target_y):
    move(target_x, target_y)


screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()
loop_counter = 0

running = True

while running:
    dt = clock.tick(60)

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

    keys = pygame.key.get_pressed()

    if loop_counter == MOVEMENT_DELAY:
        loop_counter = 0
        if keys[K_LEFT]:
            move(-1, 0)
        elif keys[K_RIGHT]:
            move(1, 0)
        elif keys[K_DOWN]:
            move(0, 1)
        elif keys[K_UP]:
            move(0, - 1)

    loop_counter = loop_counter + 1

    # Flip the display
    pygame.display.update()

# Done! Time to quit.
pygame.quit()
