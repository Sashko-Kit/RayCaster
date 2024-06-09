import pygame

class Enemy:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.health = 100

    def update(self, player_x, player_y, game_map):
        dx, dy = player_x - self.x, player_y - self.y
        distance = (dx**2 + dy**2) ** 0.5
        if distance > 0:
            self.x += dx / distance
            self.y += dy / distance
            self.rect.center = (self.x, self.y)  # Update rect position

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
