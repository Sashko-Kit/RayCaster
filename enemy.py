import pygame
import math
from settings import TILE_SIZE

class Enemy:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.health = 100
        self.speed = 100  # Speed of the enemy

    def update(self, player_x, player_y, game_map):
        # Move towards the player
        dx, dy = player_x - self.x, player_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            dx, dy = dx / distance, dy / distance

            new_x = self.x + dx * self.speed * 0.01
            new_y = self.y + dy * self.speed * 0.01

            if not self.is_wall_collision(new_x, self.y, game_map):
                self.x = new_x
            if not self.is_wall_collision(self.x, new_y, game_map):
                self.y = new_y

            self.rect.center = (self.x, self.y)

    def is_wall_collision(self, x, y, game_map):
        map_x, map_y = int(x / TILE_SIZE), int(y / TILE_SIZE)
        if 0 <= map_x < len(game_map[0]) and 0 <= map_y < len(game_map):
            return game_map[map_y][map_x] == '#'
        return False

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
