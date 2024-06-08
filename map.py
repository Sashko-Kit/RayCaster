class Map:
    def __init__(self):
        self.grid = [
            '111111111111',
            '100000000001',
            '100000000001',
            '100000000001',
            '100000000001',
            '100000000001',
            '111111111111',
        ]
    
    def get_tile(self, x, y):
        return self.grid[y][x]

    def is_wall(self, x, y):
        return self.get_tile(x, y) == '1'
