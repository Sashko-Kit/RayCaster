import pygame

class Pickup:
    def __init__(self, x, y, image, type):
        self.x = x
        self.y = y
        self.image = image
        self.type = type
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.active = True  # Adding the active attribute

    def draw(self, screen):
        screen.blit(self.image, self.rect)
