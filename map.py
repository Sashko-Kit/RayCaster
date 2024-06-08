import random

def generate_map(size):
    game_map = [['#'] * size for _ in range(size)]
    
    for y in range(1, size - 1):
        for x in range(1, size - 1):
            game_map[y][x] = '.' if random.random() > 0.2 else '#'
    
    return game_map

game_map = generate_map(24)
