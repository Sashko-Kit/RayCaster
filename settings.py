import math

# Screen settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors
BLACK = (0, 0, 0)

# Map settings
MAP_SIZE = 40  # Increased map size
TILE_SIZE = 64

# Player settings
FOV = math.pi / 3
NUM_RAYS = 120
MAX_DEPTH = MAP_SIZE * TILE_SIZE
DELTA_ANGLE = FOV / NUM_RAYS
DIST = (SCREEN_WIDTH // 2) / math.tan(FOV / 2)
PROJ_COEFF = 3 * DIST * TILE_SIZE
SCALE = SCREEN_WIDTH // NUM_RAYS

# Minimap scale
MINIMAP_SCALE = 0.1