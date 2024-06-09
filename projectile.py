import pygame
import math
from settings import TILE_SIZE

class Projectile:
    def __init__(self, x, y, angle, image):
        self.x = x
        self.y = y
        self.angle = angle
        self.image = image
        self.active = True
        self.speed = 1000  # Bullet speed in pixels per second

    def update(self, dt, game_map, enemies):
        if not self.active:
            return
        
        self.x += math.cos(self.angle) * self.speed * dt
        self.y += math.sin(self.angle) * self.speed * dt

        # Check for collision with walls
        map_x, map_y = int(self.x / TILE_SIZE), int(self.y / TILE_SIZE)
        if game_map[map_y][map_x] == '#':
            self.active = False

        # Check for collision with enemies
        for enemy in enemies:
            if enemy.rect.collidepoint(self.x, self.y):
                if enemy.take_damage(20):  # Arbitrary damage value
                    enemies.remove(enemy)
                self.active = False
                pygame.mixer.Sound('assets/sounds/hurt.mp3').play()  # Play hurt sound
                break

    def draw(self, screen):
        if self.active:
            bullet_rect = self.image.get_rect(center=(self.x, self.y))
            screen.blit(self.image, bullet_rect)
