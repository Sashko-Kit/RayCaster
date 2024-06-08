import pygame
import math
from settings import *
from map import game_map

class Player:
    def __init__(self):
        self.x, self.y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.angle = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        speed = 5
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dx += cos_a * speed
            dy += sin_a * speed
        if keys[pygame.K_s]:
            dx -= cos_a * speed
            dy -= sin_a * speed
        if keys[pygame.K_a]:
            dx += sin_a * speed
            dy -= cos_a * speed
        if keys[pygame.K_d]:
            dx -= sin_a * speed
            dy += cos_a * speed

        if self.check_wall_collision(dx, dy):
            self.x += dx
            self.y += dy
        
        if keys[pygame.K_LEFT]:
            self.angle -= 0.05
        if keys[pygame.K_RIGHT]:
            self.angle += 0.05

    def check_wall_collision(self, dx, dy):
        next_x = self.x + dx
        next_y = self.y + dy
        map_x = int(next_x / TILE_SIZE)
        map_y = int(next_y / TILE_SIZE)
        if game_map[map_y][map_x] == '#':
            return False
        return True
