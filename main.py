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

MOVEMENT_DELAY = 6

# Game states
MENU = 0
PLAYING = 1
HOW_TO_PLAY = 2

grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

current_bag = []
next_bag = shapes.SHAPES[:]
random.shuffle(next_bag)

current_piece = None
piece_x = 0
piece_y = 0
piece_rotation = 0

hold_piece = None

score = 0
paused = False
game_over = False


def new_bag():
    global current_bag, next_bag
    current_bag = next_bag
    next_bag = shapes.SHAPES[:]
    random.shuffle(next_bag)


def new_piece():
    global current_piece, piece_y, piece_x, piece_rotation, game_over

    if not len(current_bag):
        new_bag()

    current_piece = current_bag.pop()

    piece_rotation = 0
    piece_x = GRID_COLS // 2 - 1
    piece_y = 0
    if check_collision(piece_x, piece_y, piece_rotation):
        game_over = True


def check_collision(x, y, rotation) -> bool:
    if current_piece is None or paused or game_over:
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
    if current_piece is None or paused or game_over:
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
    if current_piece is None or paused or game_over:
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


def drop():
    if game_over or paused:
        return
    while move(0, 1):
        pass
    lock_piece()


def lock_piece():
    global score
    if current_piece is None:
        return
    shape = current_piece['rotations'][piece_rotation]
    color = current_piece['color']
    for dx, dy in shape:
        x = piece_x + dx
        y = piece_y + dy
        if 0 <= x < GRID_COLS and 0 <= y < GRID_ROWS:
            grid[y][x] = color

    lines_cleared = clear_lines()
    score += lines_cleared * 100
    new_piece()


def clear_lines():
    lines_cleared = 0
    for y in range(GRID_ROWS - 1, -1, -1):
        if all(grid[y][x] != 0 for x in range(GRID_COLS)):
            del grid[y]
            grid.insert(0, [0] * GRID_COLS)
            lines_cleared += 1
    return lines_cleared


def hold():
    global hold_piece, current_piece, piece_rotation, game_over
    if not hold_piece:
        hold_piece = current_piece
        new_piece()
    else:
        current_piece, hold_piece = hold_piece, current_piece
        piece_rotation = 0
        if check_collision(piece_x, piece_y, piece_rotation):
            game_over = True


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
    if current_piece and not game_over:
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


def draw_hold_piece():
    y_offset = PLAY_OFFSET_Y + BLOCK_GAP + 64
    x_offset = PLAY_OFFSET_X - BLOCK_GAP - BLOCK_SIZE * 3

    font = pygame.font.Font('Pixica-Bold.ttf', 64)
    text = font.render('Hold', True, colors.WHITE)
    screen.blit(text, (
        x_offset - BLOCK_SIZE,
        PLAY_OFFSET_Y + BLOCK_GAP
    ))

    if not hold_piece:
        return
    color = hold_piece['color']
    shape = hold_piece['rotations'][0]

    for dx, dy in shape:
        x = dx
        y = dy
        pygame.draw.rect(screen, color, (
            x * BLOCK_SIZE + x_offset,
            y * BLOCK_SIZE + y_offset,
            BLOCK_SIZE - BLOCK_GAP,
            BLOCK_SIZE - BLOCK_GAP
        ))


def draw_next_pieces_preview():
    y_offset = PLAY_OFFSET_Y + BLOCK_GAP + 64
    x_offset = PLAY_OFFSET_X + PLAY_WIDTH + BLOCK_GAP + BLOCK_SIZE * 2

    font = pygame.font.Font('Pixica-Bold.ttf', 64)
    text = font.render('Next', True, colors.WHITE)
    screen.blit(text, (
        x_offset - BLOCK_SIZE,
        PLAY_OFFSET_Y + BLOCK_GAP
    ))

    next_pieces = reversed(next_bag + current_bag)
    preview_number = 0

    for piece in next_pieces:
        if preview_number >= 5:
            break
        color = piece['color']
        shape = piece['rotations'][0]
        for dx, dy in shape:
            x = dx
            y = dy
            pygame.draw.rect(screen, color, (
                x * BLOCK_SIZE + x_offset,
                y * BLOCK_SIZE + y_offset,
                BLOCK_SIZE - BLOCK_GAP,
                BLOCK_SIZE - BLOCK_GAP
            ))

        y_offset += BLOCK_SIZE * 2.5
        preview_number += 1


def draw_score():
    y_offset = PLAY_OFFSET_Y + PLAY_HEIGHT - 32
    x_offset = PLAY_OFFSET_X + PLAY_WIDTH + BLOCK_SIZE

    font = pygame.font.Font('Pixica-Regular.ttf', 32)
    text = font.render('Score: ' + str(score), True, colors.WHITE)
    screen.blit(text, (
        x_offset,
        y_offset
    ))


def draw_pause_menu():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    font = pygame.font.Font('Pixica-Bold.ttf', 74)
    text = font.render('PAUSED', True, colors.WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(text, text_rect)
    font = pygame.font.Font('Pixica-Regular.ttf', 36)
    text = font.render('Press P to Resume', True, colors.WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(text, text_rect)
    text = font.render('Press ESC to Main Menu', True, colors.WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    screen.blit(text, text_rect)


def draw_game_over():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    font = pygame.font.Font('Pixica-Bold.ttf', 74)
    text = font.render('GAME OVER', True, colors.RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(text, text_rect)
    font = pygame.font.Font('Pixica-Regular.ttf', 36)
    text = font.render(f'Score: {score}', True, colors.WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(text, text_rect)

    text = font.render('Press R to Reset Game', True, colors.WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    screen.blit(text, text_rect)

    text = font.render('Press ESC to Main Menu', True, colors.WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
    screen.blit(text, text_rect)


def draw_main_menu():
    screen.fill(colors.BLACK)
    font = pygame.font.Font('Pixica-Bold.ttf', 100)
    title = font.render('TETRIS', True, colors.CYAN)
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
    screen.blit(title, title_rect)

    font = pygame.font.Font('Pixica-Regular.ttf', 50)
    menu_options = ["Start Game", "How to Play", "Quit"]
    for i, option in enumerate(menu_options):
        color = colors.WHITE if i == menu_selection else colors.GRAY
        text = font.render(option, True, color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + i*60))
        screen.blit(text, text_rect)


def draw_instructions():
    screen.fill(colors.BLACK)
    font = pygame.font.Font('Pixica-Regular.ttf', 32)
    lines = [
        "Controls:",
        "Left/Right Arrow - Move piece",
        "Up Arrow - Rotate piece",
        "Down Arrow - Soft drop",
        "Space - Hard drop",
        "P - Pause/Unpause",
        "ESC - Quit to menu",
        "",
        "Press Q, ESC or ENTER to return to main menu"
    ]

    for i, line in enumerate(lines):
        text = font.render(line, True,colors.WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100 + i * 40))
        screen.blit(text, text_rect)


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

# new_piece()

game_state = MENU
menu_selection = 0

running = True


def reset_game():
    global grid
    global hold_piece, current_piece, piece_x, piece_y, piece_rotation
    global score, game_state
    global current_bag, next_bag
    global paused, game_over

    grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

    current_piece = None
    hold_piece = None
    piece_x = 0
    piece_y = 0
    piece_rotation = 0

    score = 0
    game_state = PLAYING

    current_bag = []
    next_bag = shapes.SHAPES[:]
    random.shuffle(next_bag)

    paused = False
    game_over = False

    new_piece()


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
            if game_state == MENU:
                if event.key == pygame.K_DOWN:
                    menu_selection = (menu_selection + 1) % 3
                elif event.key == pygame.K_UP:
                    menu_selection = (menu_selection - 1) % 3
                elif event.key == pygame.K_RETURN:
                    if menu_selection == 0:  # Start Game
                        reset_game()
                    elif menu_selection == 1:  # How to Play
                        game_state = HOW_TO_PLAY
                    elif menu_selection == 2:  # Quit
                        running = False

            elif game_state == PLAYING:
                if not game_over:
                    if paused:
                        if event.key == pygame.K_ESCAPE:
                            game_state = MENU
                        if event.key == pygame.K_p:
                            paused = not paused
                    elif event.key == pygame.K_ESCAPE:
                        paused = not paused
                    elif event.key == pygame.K_p:
                        paused = not paused
                    elif event.key == pygame.K_SPACE:
                        drop()
                    elif event.key == pygame.K_LEFT:
                        move(-1, 0)
                    elif event.key == K_RIGHT:
                        move(1, 0)
                    elif event.key == K_DOWN:
                        move(0, 1)
                    elif event.key == K_UP:
                        rotate()
                    elif event.key == K_c:
                        hold()
                else:
                    if event.key == pygame.K_r:
                        reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        game_state = MENU

            elif game_state == HOW_TO_PLAY:
                if event.key == pygame.K_q:
                    game_state = MENU
                elif event.key == pygame.K_ESCAPE:
                    game_state = MENU
                elif event.key == pygame.K_RETURN:
                    game_state = MENU


    if game_state == MENU:
        draw_main_menu()
    elif game_state == PLAYING:

        # Game logic
        if not game_over and not paused:
            if current_time - fall_time >= fall_speed:
                if not move(0, 1):
                    lock_piece()
                fall_time = current_time

            # Movement
            if not game_over:
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

                if down_duration == MOVEMENT_DELAY / 2:
                    down_duration = 0
                    move(0, 1)

        # Drawing
        draw_grid()
        draw_pieces()
        draw_next_pieces_preview()
        draw_hold_piece()
        draw_score()
        if paused:
            draw_pause_menu()
        if game_over:
            draw_game_over()
    elif game_state == HOW_TO_PLAY:
        draw_instructions()



    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
