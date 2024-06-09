import pygame

class Pickup:
    def __init__(self, x, y, image, pickup_type):
        self.x = x
        self.y = y
        self.image = image
        self.type = pickup_type
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
