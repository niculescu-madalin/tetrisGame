import random
from pygame.locals import *
import shapes

from rendering import *
from controls import *

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


pygame.init()

# Initialize controllers
pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    controller = pygame.joystick.Joystick(0)
    controller.init()
else:
    controller = None


print(controller)
if controller.get_numhats() > 0:
    print("D-Pad is available")


BUTTON_A = 0        # Drop
BUTTON_B = 1        # Rotate
BUTTON_X = 2        # Hold
BUTTON_Y = 3        # Pause
BUTTON_START = 7    # Start/Menu
BUTTON_BACK = 6     # Back/Menu

AXIS_LEFT_X = 0
AXIS_LEFT_Y = 1


# create screen
screen = init_screen()
# initialize clock
clock = pygame.time.Clock()

game_state = MENU
menu_selection = 0
paused = False
game_over = False

score = 0

grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

current_bag = []
next_bag = shapes.SHAPES[:]
random.shuffle(next_bag)

current_piece = None
hold_piece = None
piece_x = 0
piece_y = 0
piece_rotation = 0

fall_time = 0
fall_speed = 500

left_duration = 0
right_duration = 0
down_duration = 0

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

        elif event.type == pygame.KEYDOWN:
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

        elif event.type == pygame.JOYHATMOTION:
            hat_x, hat_y = event.value
            if game_state == MENU:
                if hat_y == 1:
                    menu_selection = (menu_selection - 1) % 3
                if hat_y == -1:
                    menu_selection = (menu_selection + 1) % 3

            elif game_state == PLAYING and not paused and not game_over:
                if hat_x == -1:
                    move(-1, 0)
                elif hat_x == 1:
                    move(1, 0)

                if hat_y == -1:  # D-pad down
                    move(0, 1)
                elif hat_y == 1:  # D-pad up = rotate
                    rotate()

        # Controller button press
        elif event.type == pygame.JOYBUTTONDOWN:
            if game_state == MENU:
                if event.button == BUTTON_B:
                    if menu_selection == 0:
                        reset_game()
                    elif menu_selection == 1:
                        game_state = HOW_TO_PLAY
                    elif menu_selection == 2:
                        running = False

            elif game_state == PLAYING:
                if not game_over:
                    if paused:
                        if event.button == BUTTON_Y:
                            paused = not paused
                    else:
                        if event.button == BUTTON_Y:
                            paused = not paused
                        elif event.button == BUTTON_A:
                            drop()
                        elif event.button == BUTTON_B:
                            rotate()
                        elif event.button == BUTTON_X:
                            hold()
                else:
                    if event.button == BUTTON_BACK:
                        game_state = MENU
                    elif event.button == BUTTON_A:
                        reset_game()

            elif game_state == HOW_TO_PLAY:
                if event.button in [BUTTON_BACK, BUTTON_Y, BUTTON_A]:
                    game_state = MENU

        # Optional: Controller axis motion for movement
        elif event.type == pygame.JOYAXISMOTION:
            if game_state == PLAYING and not paused and not game_over:
                if event.axis == AXIS_LEFT_X:
                    if event.value < -0.5:
                        move(-1, 0)
                    elif event.value > 0.5:
                        move(1, 0)
                elif event.axis == AXIS_LEFT_Y:
                    if event.value > 0.5:
                        move(0, 1)

    if game_state == MENU:
        draw_main_menu(screen, menu_selection)
    elif game_state == PLAYING:
        # Game logic
        if not game_over and not paused:
            if current_time - fall_time >= fall_speed:
                if not move(0, 1):
                    lock_piece()
                fall_time = current_time

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

            if down_duration == MOVEMENT_DELAY / 2:
                down_duration = 0
                move(0, 1)



        # Drawing
        draw_grid(screen, grid)
        draw_pieces()
        draw_next_pieces(screen, current_bag, next_bag)
        draw_hold_piece(screen, hold_piece)
        draw_score(screen, score)
        if paused:
            draw_pause_menu(screen)
        if game_over:
            draw_game_over(screen, score)
    elif game_state == HOW_TO_PLAY:
        draw_instructions(screen)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
