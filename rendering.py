import colors
from constants import *
from colors import *


def init_screen():
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("Tetris")
    return screen


def draw_grid(screen, grid):
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
                pygame.draw.rect(screen, BEAVER_800, (
                    PLAY_OFFSET_X + BLOCK_GAP + x * BLOCK_SIZE,
                    PLAY_OFFSET_Y + BLOCK_GAP + y * BLOCK_SIZE,
                    BLOCK_SIZE - BLOCK_GAP,
                    BLOCK_SIZE - BLOCK_GAP
                ))


def draw_current_piece(screen, game_state):
    if game_state.current_piece and not game_state.game_over:
        color = game_state.current_piece['color']
        shape = game_state.current_piece['rotations'][game_state.piece_rotation]

        for dx, dy in shape:
            x = game_state.piece_x + dx
            y = game_state.piece_y + dy
            if 0 <= x < GRID_COLS and 0 <= y < GRID_ROWS:
                pygame.draw.rect(screen, color, (
                    PLAY_OFFSET_X + BLOCK_GAP + x * BLOCK_SIZE,
                    PLAY_OFFSET_Y + BLOCK_GAP + y * BLOCK_SIZE,
                    BLOCK_SIZE - BLOCK_GAP,
                    BLOCK_SIZE - BLOCK_GAP
                ))


def draw_hold_piece(screen, hold_piece):
    y_offset = PLAY_OFFSET_Y + BLOCK_GAP + 64
    x_offset = PLAY_OFFSET_X - BLOCK_GAP - BLOCK_SIZE * 3

    font = pygame.font.Font('assets/Pixica-Bold.ttf', 64)
    text = font.render('Hold', True, WHITE)
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


def draw_next_pieces(screen, current_bag, next_bag):
    y_offset = PLAY_OFFSET_Y + BLOCK_GAP + 64
    x_offset = PLAY_OFFSET_X + PLAY_WIDTH + BLOCK_GAP + BLOCK_SIZE * 2

    font = pygame.font.Font('assets/Pixica-Bold.ttf', 64)
    text = font.render('Next', True, WHITE)
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


def draw_score(screen, score):
    y_offset = PLAY_OFFSET_Y + PLAY_HEIGHT - 32
    x_offset = PLAY_OFFSET_X + PLAY_WIDTH + BLOCK_SIZE

    font = pygame.font.Font('assets/Pixica-Regular.ttf', 32)
    text = font.render('Score: ' + str(score), True, WHITE)
    screen.blit(text, (
        x_offset,
        y_offset
    ))


def draw_pause_menu(screen):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))

    font = pygame.font.Font('assets/Pixica-Bold.ttf', 74)
    text = font.render('PAUSED', True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    font = pygame.font.Font('assets/Pixica-Regular.ttf', 36)
    text = font.render('Press P to Resume', True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(text, text_rect)

    text = font.render('Press ESC to Main Menu', True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    screen.blit(text, text_rect)


def draw_game_over(screen, score):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))

    font = pygame.font.Font('assets/Pixica-Bold.ttf', 74)
    text = font.render('GAME OVER', True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    font = pygame.font.Font('assets/Pixica-Regular.ttf', 36)
    text = font.render(f'Score: {score}', True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(text, text_rect)

    text = font.render('Press R to Reset Game', True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    screen.blit(text, text_rect)

    text = font.render('Press ESC to Main Menu', True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
    screen.blit(text, text_rect)


def draw_main_menu(screen, menu_selection):
    screen.fill(BLACK)
    font = pygame.font.Font('assets/Pixica-Bold.ttf', 100)
    title = font.render('TETRIS', True, CYAN)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title, title_rect)

    font = pygame.font.Font('assets/Pixica-Regular.ttf', 50)
    menu_options = ["Start Game", "How to Play", "Quit"]
    for i, option in enumerate(menu_options):
        color = WHITE if i == menu_selection else GRAY
        text = font.render(option, True, color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 60))
        screen.blit(text, text_rect)


def draw_instructions(screen):
    screen.fill(BLACK)
    font = pygame.font.Font('assets/Pixica-Regular.ttf', 32)
    lines = [
        "Controls:",
        "Left/Right Arrow - Move piece",
        "Up Arrow - Rotate piece",
        "Down Arrow - Soft drop",
        "Space - Hard drop",
        "P or ESC - Pause Menu",
        "",
        "",
        "Press Q, ESC or ENTER to return to main menu"
    ]

    for i, line in enumerate(lines):
        text = font.render(line, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100 + i * 40))
        screen.blit(text, text_rect)


def draw_game(screen, game_state):
    draw_grid(screen, game_state.grid)
    draw_current_piece(screen, game_state)
    draw_next_pieces(screen, game_state.current_bag, game_state.next_bag)
    draw_hold_piece(screen, game_state.hold_piece)
    draw_score(screen, game_state.score)

    if game_state.paused:
        draw_pause_menu(screen)
    if game_state.game_over:
        draw_game_over(screen, game_state.score)
