import pygame
import math
from settings import *

class RayCasting:
    def __init__(self, screen, player, game_map):
        self.screen = screen
        self.player = player
        self.game_map = game_map

    def cast_ray(self, angle):
        ox, oy = self.player.get_position()  # Use bobbing position
        dx, dy = math.cos(angle), math.sin(angle)

        for depth in range(MAX_DEPTH):
            target_x = ox + dx * depth
            target_y = oy + dy * depth

            col = int(target_x // TILE_SIZE)
            row = int(target_y // TILE_SIZE)

            if self.game_map.is_wall(col, row):
                hit_x = target_x - col * TILE_SIZE
                hit_y = target_y - row * TILE_SIZE

                if 0 <= hit_x < TILE_SIZE and 0 <= hit_y < TILE_SIZE:
                    return depth, (col, row)
        
        return MAX_DEPTH, None

    def render(self):
        for ray in range(SCREEN_WIDTH):
            ray_angle = (self.player.get_angle() - FOV // 2 + (ray / SCREEN_WIDTH) * FOV)
            distance, wall_coords = self.cast_ray(math.radians(ray_angle))

            wall_height = min(int(SCREEN_HEIGHT / (distance + 0.0001) * TILE_SIZE), SCREEN_HEIGHT)

            color = (255 / (1 + distance * distance * 0.0001),) * 3
            pygame.draw.rect(self.screen, color, (ray, SCREEN_HEIGHT // 2 - wall_height // 2, 1, wall_height))
