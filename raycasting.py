import pygame
import math
from settings import *

def ray_casting(screen, player, game_map, wall_texture):
    ox, oy = player.x, player.y
    xm, ym = MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE
    cur_angle = player.angle - FOV / 2
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        for depth in range(1, MAX_DEPTH):  # start from 1 to avoid division by zero
            x = ox + depth * cos_a
            y = oy + depth * sin_a
            if 0 < x < xm and 0 < y < ym:
                map_x, map_y = int(x / TILE_SIZE), int(y / TILE_SIZE)
                if game_map[map_y][map_x] == '#':
                    depth *= math.cos(player.angle - cur_angle)
                    proj_height = PROJ_COEFF / depth
                    wall_column = pygame.transform.scale(wall_texture, (SCALE, int(proj_height)))
                    screen.blit(wall_column, (ray * SCALE, SCREEN_HEIGHT // 2 - proj_height // 2))
                    break
        cur_angle += DELTA_ANGLE
