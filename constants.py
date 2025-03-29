# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Grid dimensions
GRID_COLS = 10
GRID_ROWS = 20
BLOCK_SIZE = 32
BLOCK_GAP = 3

# Play area dimensions
PLAY_WIDTH = BLOCK_SIZE * GRID_COLS
PLAY_HEIGHT = BLOCK_SIZE * GRID_ROWS
PLAY_OFFSET_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
PLAY_OFFSET_Y = (SCREEN_HEIGHT - PLAY_HEIGHT) // 2

# Game mechanics
MOVEMENT_DELAY = 6
FALL_SPEED = 500

# File paths
FONT_BOLD = 'assets/fonts/Pixica-Bold.ttf'
FONT_REGULAR = 'assets/fonts/Pixica-Regular.ttf'

# Game states
MENU = 0
PLAYING = 1
HOW_TO_PLAY = 2