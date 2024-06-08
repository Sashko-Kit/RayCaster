import pygame
import math
from settings import *

def ray_casting(screen, player, game_map):
    ox, oy = player.x, player.y
    xm, ym = MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE
    cur_angle = player.angle - FOV / 2
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        for depth in range(MAX_DEPTH):
            x = ox + depth * cos_a
            y = oy + depth * sin_a
            if 0 < x < xm and 0 < y < ym:
                map_x, map_y = int(x / TILE_SIZE), int(y / TILE_SIZE)
                if game_map[map_y * MAP_WIDTH + map_x] == '#':
                    depth *= math.cos(player.angle - cur_angle)
                    proj_height = PROJ_COEFF / depth
                    color = [255 / (1 + depth * depth * 0.0001)] * 3
                    pygame.draw.rect(screen, color, (ray * SCALE, SCREEN_HEIGHT // 2 - proj_height // 2, SCALE, proj_height))
                    break
        cur_angle += DELTA_ANGLE
