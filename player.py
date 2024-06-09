import pygame
import math
from settings import *
from map import game_map
import random

class Player:
    def __init__(self):
        self.x, self.y = self.find_valid_spawn()
        self.angle = 0
        self.health = 100  # Player's health
        self.speed = 5
        self.speed_timer = 0
        self.damage_cooldown = 0  # Timer for damage cooldown

    def find_valid_spawn(self):
        while True:
            x = random.randint(1, MAP_SIZE - 1) * TILE_SIZE + TILE_SIZE // 2
            y = random.randint(1, MAP_SIZE - 1) * TILE_SIZE + TILE_SIZE // 2
            map_x = int(x / TILE_SIZE)
            map_y = int(y / TILE_SIZE)
            if game_map[map_y][map_x] == '.':
                return x, y

    def movement(self):
        keys = pygame.key.get_pressed()
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dx += cos_a * self.speed
            dy += sin_a * self.speed
        if keys[pygame.K_s]:
            dx -= cos_a * self.speed
            dy -= sin_a * self.speed
        if keys[pygame.K_a]:
            dx += sin_a * self.speed
            dy -= cos_a * self.speed
        if keys[pygame.K_d]:
            dx -= sin_a * self.speed
            dy += cos_a * self.speed

        if self.check_wall_collision(dx, dy):
            self.x += dx
            self.y += dy
        
        if keys[pygame.K_LEFT]:
            self.angle -= 0.05
        if keys[pygame.K_RIGHT]:
            self.angle += 0.05

        # Update speed timer
        if self.speed_timer > 0:
            self.speed_timer -= 1
        else:
            self.speed = 5

        # Update damage cooldown timer
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

    def check_wall_collision(self, dx, dy):
        next_x = self.x + dx
        next_y = self.y + dy
        map_x = int(next_x / TILE_SIZE)
        map_y = int(next_y / TILE_SIZE)
        if game_map[map_y][map_x] == '#':
            return False
        return True

    def take_damage(self, amount):
        if self.damage_cooldown <= 0:
            self.health -= amount
            if self.health < 0:
                self.health = 0
            self.damage_cooldown = FPS * 2  # 2 seconds cooldown

    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100

    def speed_up(self):
        self.speed = 10
        self.speed_timer = FPS * 5  # Speed up for 5 seconds
