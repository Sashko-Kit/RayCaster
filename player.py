import pygame
import math
from settings import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, ROTATION_SPEED, MOVE_SPEED, BOBBING_SPEED, BOBBING_AMOUNT

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.bobbing_offset = 0
        self.bobbing_direction = 1

    def update(self, map):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # Rotate left
            self.angle -= ROTATION_SPEED
        if keys[pygame.K_d]:  # Rotate right
            self.angle += ROTATION_SPEED
        if keys[pygame.K_w]:  # Move forward
            self.move(MOVE_SPEED, map)
        if keys[pygame.K_s]:  # Move backward
            self.move(-MOVE_SPEED, map)

    def move(self, distance, map):
        dx = distance * math.cos(math.radians(self.angle))
        dy = distance * math.sin(math.radians(self.angle))

        new_x = self.x + dx
        new_y = self.y + dy

        if not map.is_wall(int(new_x // TILE_SIZE), int(new_y // TILE_SIZE)):
            self.x = new_x
            self.y = new_y
            self.bob()  # Update bobbing effect

    def bob(self):
        # Bobbing effect logic
        self.bobbing_offset += BOBBING_SPEED * self.bobbing_direction
        if abs(self.bobbing_offset) > BOBBING_AMOUNT:
            self.bobbing_direction *= -1

    def get_position(self):
        # Return position with bobbing effect
        bob_y = self.y + self.bobbing_offset
        return self.x, bob_y

    def get_angle(self):
        return self.angle
