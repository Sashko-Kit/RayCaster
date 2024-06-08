import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK  # Explicitly import BLACK and other constants
from player import Player
from raycasting import ray_casting
from map import game_map

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        player.movement()
        screen.fill(BLACK)
        ray_casting(screen, player, game_map)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()