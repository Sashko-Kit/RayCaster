import math

# Screen settings
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60

# Colors
BLACK = (0, 0, 0)

# Map settings
MAP_WIDTH = 8
MAP_HEIGHT = 8
TILE_SIZE = 64

# Player settings
FOV = math.pi / 3
NUM_RAYS = 120
MAX_DEPTH = MAP_WIDTH * TILE_SIZE
DELTA_ANGLE = FOV / NUM_RAYS
DIST = (SCREEN_WIDTH // 2) / math.tan(FOV / 2)
PROJ_COEFF = 3 * DIST * TILE_SIZE
SCALE = SCREEN_WIDTH // NUM_RAYS
