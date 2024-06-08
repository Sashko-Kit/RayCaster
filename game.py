import pygame
from settings import *
from player import Player
from map import Map
from raycasting import RayCasting

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.map = Map()
        x, y = self.map.get_random_empty_position()
        self.player = Player(x, y)
        self.ray_casting = RayCasting(self.screen, self.player, self.map)
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.player.update(self.map)
            self.screen.fill(BLACK)
            self.ray_casting.render()
            pygame.display.flip()
            self.clock.tick(FPS)

  
