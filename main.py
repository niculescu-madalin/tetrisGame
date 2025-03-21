import random
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
grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
current_piece = None
piece_x = 0
piece_y = 0
piece_rotation = 0

game_over = False


def new_piece():
    global current_piece, piece_y, piece_x, piece_rotation, game_over
    current_piece = random.choice(shapes.SHAPES)
    piece_rotation = 0
    piece_x = GRID_COLS // 2 - 1
    piece_y = 0
    if check_collision(piece_x, piece_y, piece_rotation):
        game_over = True


def check_collision(x, y, rotation) -> bool:
    if current_piece is None:
        return True
    shape = current_piece['rotations'][rotation]
    for dx, dy in shape:
        new_x = x + dx
        new_y = y + dy
        if new_x < 0 or new_x >= GRID_COLS or new_y >= GRID_ROWS:
            return True
        if new_y >= 0 and grid[new_y][new_x]:
            return True
    return False


def move(dx, dy):
    global piece_x, piece_y
    if current_piece is None or game_over:
        return False
    new_x = piece_x + dx
    new_y = piece_y + dy
    if not check_collision(new_x, new_y, piece_rotation):
        piece_x = new_x
        piece_y = new_y
        return True
    return False


def rotate():
    global piece_x, piece_y, piece_rotation
    if current_piece is None:
        return

    # get a new rotation from the possible oness
    new_rotation = (piece_rotation + 1) % len(current_piece['rotations'])
    if not check_collision(piece_x, piece_y, new_rotation):
        piece_rotation = new_rotation
    else:
        if not check_collision(piece_x - 1, piece_y, new_rotation):
            piece_rotation = new_rotation
            piece_x -= 1
        elif not check_collision(piece_x + 1, piece_y, new_rotation):
            piece_rotation = new_rotation
            piece_x += 1


def lock_piece():
    if current_piece is None:
        return
    shape = current_piece['rotations'][piece_rotation]
    color = current_piece['color']
    for dx, dy in shape:
        x = piece_x + dx
        y = piece_y + dy
        if 0 <= x < GRID_COLS and 0 <= y < GRID_ROWS:
            grid[y][x] = color
    new_piece()


def draw_grid():
    pygame.draw.rect(screen, colors.BEAVER_300, (
        PLAY_OFFSET_X,
        PLAY_OFFSET_Y,
        PLAY_WIDTH + BLOCK_GAP,
        PLAY_HEIGHT + BLOCK_GAP
    ))

    for y in range(GRID_ROWS):
        for x in range(GRID_COLS):
            color = grid[y][x]
            if color:
                pygame.draw.rect(screen, color, (
                    PLAY_OFFSET_X + BLOCK_GAP + x * BLOCK_SIZE,
                    PLAY_OFFSET_Y + BLOCK_GAP + y * BLOCK_SIZE,
                    BLOCK_SIZE - BLOCK_GAP,
                    BLOCK_SIZE - BLOCK_GAP
                ))
            else:
                pygame.draw.rect(screen, colors.BEAVER_800, (
                    PLAY_OFFSET_X + BLOCK_GAP + x * BLOCK_SIZE,
                    PLAY_OFFSET_Y + BLOCK_GAP + y * BLOCK_SIZE,
                    BLOCK_SIZE - BLOCK_GAP,
                    BLOCK_SIZE - BLOCK_GAP
                ))


def draw_pieces():
    color = current_piece['color']
    shape = current_piece['rotations'][piece_rotation]
    for dx, dy in shape:
        x = piece_x + dx
        y = piece_y + dy
        if 0 <= x < GRID_COLS and 0 <= y < GRID_ROWS:
            pygame.draw.rect(screen, color, (
                PLAY_OFFSET_X + BLOCK_GAP + x * BLOCK_SIZE,
                PLAY_OFFSET_Y + BLOCK_GAP + y * BLOCK_SIZE,
                BLOCK_SIZE - BLOCK_GAP,
                BLOCK_SIZE - BLOCK_GAP
            ))


# create screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Tetris")
fall_time = 0
fall_speed = 500

# initialize clock
clock = pygame.time.Clock()

left_duration = 0
right_duration = 0
down_duration = 0

new_piece()

running = True

while running:
    screen.fill(colors.BLACK)
    dt = clock.tick(60)
    current_time = pygame.time.get_ticks()

    # Piece movement
    keys = pygame.key.get_pressed()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                new_piece()
            elif event.key == pygame.K_LEFT:
                move(-1, 0)
            elif event.key == K_RIGHT:
                move(1, 0)
            elif event.key == K_DOWN:
                move(0, 1)
            elif event.key == K_UP:
                rotate()

    # Movement
    if keys[K_LEFT]:
        left_duration = left_duration + 1
    else:
        left_duration = 0

    if keys[K_RIGHT]:
        right_duration = right_duration + 1
    else:
        right_duration = 0

    if keys[K_DOWN]:
        down_duration = down_duration + 1
    else:
        down_duration = 0

    if left_duration == MOVEMENT_DELAY:
        left_duration = 0
        move(-1, 0)

    if right_duration == MOVEMENT_DELAY:
        right_duration = 0
        move(1, 0)

    if down_duration == MOVEMENT_DELAY:
        down_duration = 0
        move(0, 1)

    # Game logic
    if current_time - fall_time >= fall_speed:
        if not move(0, 1):
            lock_piece()
        fall_time = current_time

    # Drawing
    draw_grid()
    draw_pieces()

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
