import random

def generate_map(size):
    game_map = [['#'] * size for _ in range(size)]
    
    def add_room(x, y, w, h):
        for i in range(y, y + h):
            for j in range(x, x + w):
                if 0 <= i < size and 0 <= j < size:
                    game_map[i][j] = '.'

    def add_corridor(x1, y1, x2, y2):
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                game_map[y][x1] = '.'
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                game_map[y1][x] = '.'
    
    num_rooms = 20  # Increased number of rooms for a larger map
    rooms = []
    
    for _ in range(num_rooms):
        w = random.randint(4, 8)
        h = random.randint(4, 8)
        x = random.randint(1, size - w - 1)
        y = random.randint(1, size - h - 1)
        
        add_room(x, y, w, h)
        if rooms:
            last_room_x, last_room_y = rooms[-1]
            add_corridor(last_room_x, last_room_y, x + w // 2, last_room_y)
            add_corridor(x + w // 2, last_room_y, x + w // 2, y + h // 2)
        rooms.append((x + w // 2, y + h // 2))

    return game_map

game_map = generate_map(40)  # Increased map size
