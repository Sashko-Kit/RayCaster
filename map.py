import random
from settings import TILE_SIZE

class Map:
    def __init__(self, width=12, height=12):
        self.width = width
        self.height = height
        self.grid = self.generate_random_map()

    def generate_random_map(self):
        grid = [['1' if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1 else '0'
                 for x in range(self.width)] for y in range(self.height)]

        for _ in range(int(self.width * self.height * 0.2)):  # 20% walls
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            grid[y][x] = '1'
        return grid

    def get_tile(self, x, y):
        return self.grid[y][x]

    def is_wall(self, x, y):
        return self.get_tile(x, y) == '1'

    def get_random_empty_position(self):
        while True:
            x = random.randint(1, self.width - 2) * TILE_SIZE + TILE_SIZE // 2
            y = random.randint(1, self.height - 2) * TILE_SIZE + TILE_SIZE // 2
            if not self.is_wall(x // TILE_SIZE, y // TILE_SIZE):
                return x, y
