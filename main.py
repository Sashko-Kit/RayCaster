import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK
from player import Player
from raycasting import ray_casting
from map import game_map
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player()
    
    wall_texture = pygame.image.load('assets/textures/wall.png').convert()
    hand_sprite = pygame.image.load('assets/textures/caster.png').convert_alpha()

    hand_sprite = pygame.transform.scale(hand_sprite, (400, 400))  # Further enlarge the sprite

    bobbing_amplitude = 5  # Amplitude of the bobbing motion
    bobbing_frequency = 0.1  # Frequency of the bobbing motion
    bobbing_phase = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        player.movement()
        screen.fill(BLACK)
        ray_casting(screen, player, game_map, wall_texture)

        # Update bobbing phase
        if any(pygame.key.get_pressed()):  # If any key is pressed, bob faster
            bobbing_phase += bobbing_frequency * 2
        else:  # If idle, bob slower
            bobbing_phase += bobbing_frequency

        bobbing_offset = math.sin(bobbing_phase) * bobbing_amplitude

        # Draw the hand sprite with bobbing effect
        hand_sprite_rect = hand_sprite.get_rect(bottomright=(SCREEN_WIDTH, SCREEN_HEIGHT - bobbing_offset))
        screen.blit(hand_sprite, hand_sprite_rect)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
