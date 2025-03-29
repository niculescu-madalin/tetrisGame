import random
from constants import *
from shapes import SHAPES


class GameState:
    def __init__(self):
        self.game_state = MENU
        self.menu_selection = 0

        self.grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.current_bag = []
        self.next_bag = SHAPES[:]
        random.shuffle(self.next_bag)
        self.current_piece = None
        self.piece_x = 0
        self.piece_y = 0
        self.piece_rotation = 0
        self.hold_piece = None
        self.score = 0
        self.paused = False
        self.game_over = False
        self.fall_time = 0
        self.fall_speed = FALL_SPEED

        self.new_piece()

    def new_bag(self):
        self.current_bag = self.next_bag
        self.next_bag = SHAPES[:]
        random.shuffle(self.next_bag)

    def new_piece(self):
        if not len(self.current_bag):
            self.new_bag()

        self.current_piece = self.current_bag.pop()
        self.piece_rotation = 0
        self.piece_x = GRID_COLS // 2 - 1
        self.piece_y = 0

        if self.check_collision(self.piece_x, self.piece_y, self.piece_rotation):
            self.game_over = True

    def check_collision(self, x, y, rotation) -> bool:
        if self.current_piece is None or self.paused or self.game_over:
            return True

        shape = self.current_piece['rotations'][rotation]
        for dx, dy in shape:
            new_x = x + dx
            new_y = y + dy
            if new_x < 0 or new_x >= GRID_COLS or new_y >= GRID_ROWS:
                return True
            if new_y >= 0 and self.grid[new_y][new_x]:
                return True
        return False

    def move(self, dx, dy):
        if self.current_piece is None or self.paused or self.game_over:
            return False

        new_x = self.piece_x + dx
        new_y = self.piece_y + dy
        if not self.check_collision(new_x, new_y, self.piece_rotation):
            self.piece_x = new_x
            self.piece_y = new_y
            return True
        return False

    def rotate(self):
        if self.current_piece is None or self.paused or self.game_over:
            return

        new_rotation = (self.piece_rotation + 1) % len(self.current_piece['rotations'])
        if not self.check_collision(self.piece_x, self.piece_y, new_rotation):
            self.piece_rotation = new_rotation
        else:
            if not self.check_collision(self.piece_x - 1, self.piece_y, new_rotation):
                self.piece_rotation = new_rotation
                self.piece_x -= 1
            elif not self.check_collision(self.piece_x + 1, self.piece_y, new_rotation):
                self.piece_rotation = new_rotation
                self.piece_x += 1

    def drop(self):
        if self.game_over or self.paused:
            return
        while self.move(0, 1):
            pass
        self.lock_piece()

    def lock_piece(self):
        if self.current_piece is None:
            return

        shape = self.current_piece['rotations'][self.piece_rotation]
        color = self.current_piece['color']
        for dx, dy in shape:
            x = self.piece_x + dx
            y = self.piece_y + dy
            if 0 <= x < GRID_COLS and 0 <= y < GRID_ROWS:
                self.grid[y][x] = color

        lines_cleared = self.clear_lines()
        self.score += lines_cleared * 100
        self.new_piece()

    def clear_lines(self):
        lines_cleared = 0
        for y in range(GRID_ROWS - 1, -1, -1):
            if all(self.grid[y][x] != 0 for x in range(GRID_COLS)):
                del self.grid[y]
                self.grid.insert(0, [0] * GRID_COLS)
                lines_cleared += 1
        return lines_cleared

    def hold(self):
        if not self.hold_piece:
            self.hold_piece = self.current_piece
            self.new_piece()
        else:
            self.current_piece, self.hold_piece = self.hold_piece, self.current_piece
            self.piece_rotation = 0
            if self.check_collision(self.piece_x, self.piece_y, self.piece_rotation):
                self.game_over = True

    def reset(self):
        self.__init__()