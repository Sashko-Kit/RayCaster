import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
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

            self.update()
            self.render()
            self.clock.tick(60)
        pygame.quit()

    def update(self):
        self.player.update(self.map)

    def render(self):
        self.screen.fill(pygame.Color('black'))
        self.ray_casting.render()
        self.draw_minimap()
        pygame.display.flip()

    def draw_minimap(self):
        minimap_size = 200  # Size of the minimap square
        minimap_scale = minimap_size / max(self.map.width * TILE_SIZE, self.map.height * TILE_SIZE)
        minimap_surface = pygame.Surface((minimap_size, minimap_size))
        minimap_surface.fill(pygame.Color('black'))

        for y in range(self.map.height):
            for x in range(self.map.width):
                if self.map.is_wall(x, y):
                    color = pygame.Color('gray')
                else:
                    color = pygame.Color('white')

                rect = pygame.Rect(x * TILE_SIZE * minimap_scale,
                                   y * TILE_SIZE * minimap_scale,
                                   TILE_SIZE * minimap_scale,
                                   TILE_SIZE * minimap_scale)
                pygame.draw.rect(minimap_surface, color, rect)

        player_x, player_y = self.player.get_position()
        player_rect = pygame.Rect(player_x * minimap_scale,
                                  player_y * minimap_scale,
                                  TILE_SIZE * minimap_scale / 2,
                                  TILE_SIZE * minimap_scale / 2)
        pygame.draw.rect(minimap_surface, pygame.Color('red'), player_rect)

        self.screen.blit(minimap_surface, (10, SCREEN_HEIGHT - minimap_size - 10))

if __name__ == '__main__':
    game = Game()
    game.run()
