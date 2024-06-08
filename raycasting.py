import pygame
import math
from settings import TILE_SIZE, FOV, MAX_DEPTH, TEXTURE_PATH, SCREEN_WIDTH, SCREEN_HEIGHT

class RayCasting:
    def __init__(self, screen, player, game_map):
        self.screen = screen
        self.player = player
        self.game_map = game_map
        self.wall_texture = pygame.image.load(TEXTURE_PATH).convert()
        self.texture_width = self.wall_texture.get_width()
        self.texture_height = self.wall_texture.get_height()

    def cast_ray(self, angle):
        ox, oy = self.player.get_position()
        dx, dy = math.cos(angle), math.sin(angle)

        map_x, map_y = int(ox) // TILE_SIZE, int(oy) // TILE_SIZE

        side_dist_x, side_dist_y = 0, 0
        delta_dist_x = abs(1 / dx) if dx != 0 else float('inf')
        delta_dist_y = abs(1 / dy) if dy != 0 else float('inf')
        step_x, step_y = 0, 0
        hit = False
        side = None

        if dx < 0:
            step_x = -1
            side_dist_x = (ox - map_x * TILE_SIZE) * delta_dist_x
        else:
            step_x = 1
            side_dist_x = (map_x * TILE_SIZE + TILE_SIZE - ox) * delta_dist_x

        if dy < 0:
            step_y = -1
            side_dist_y = (oy - map_y * TILE_SIZE) * delta_dist_y
        else:
            step_y = 1
            side_dist_y = (map_y * TILE_SIZE + TILE_SIZE - oy) * delta_dist_y

        while not hit:
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_x += step_x
                side = 0
            else:
                side_dist_y += delta_dist_y
                map_y += step_y
                side = 1

            if self.game_map.is_wall(map_x, map_y):
                hit = True

        if side == 0:
            perp_wall_dist = (map_x - ox + (1 - step_x) / 2) / (dx if dx != 0 else 0.0001)
        else:
            perp_wall_dist = (map_y - oy + (1 - step_y) / 2) / (dy if dy != 0 else 0.0001)

        return perp_wall_dist, (map_x, map_y), ox + perp_wall_dist * dx, oy + perp_wall_dist * dy

    def render(self):
        half_fov = math.radians(FOV / 2)
        for ray in range(SCREEN_WIDTH):
            ray_angle = math.radians(self.player.get_angle()) - half_fov + (ray / SCREEN_WIDTH) * 2 * half_fov
            distance, wall_coords, hit_x, hit_y = self.cast_ray(ray_angle)

            if wall_coords:
                corrected_distance = distance * math.cos(ray_angle - math.radians(self.player.get_angle()))
                wall_height = int(SCREEN_HEIGHT / (corrected_distance + 0.0001) * TILE_SIZE)
                wall_height = max(0, wall_height)  # Ensure wall height is not negative
                texture_x = int((hit_x % TILE_SIZE) * self.texture_width / TILE_SIZE)
                texture_column = self.wall_texture.subsurface(texture_x, 0, 1, self.texture_height)
                texture_column = pygame.transform.scale(texture_column, (1, wall_height))
                self.screen.blit(texture_column, (ray, SCREEN_HEIGHT // 2 - wall_height // 2))
            else:
                wall_height = int(SCREEN_HEIGHT / (distance + 0.0001) * TILE_SIZE)
                wall_height = max(0, wall_height)  # Ensure wall height is not negative
                color = (255 / (1 + distance * distance * 0.0001),) * 3
                pygame.draw.rect(self.screen, color, (ray, SCREEN_HEIGHT // 2 - wall_height // 2, 1, wall_height))
