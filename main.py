import pygame
import math
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, TILE_SIZE, MAP_SIZE
from player import Player
from raycasting import ray_casting
from map import game_map
from projectile import Projectile  # Import Projectile class
from enemy import Enemy  # Import Enemy class
from pickup import Pickup  # Import Pickup class

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player()
    
    wall_texture = pygame.image.load('assets/textures/wall.png').convert()
    hand_sprite = pygame.image.load('assets/textures/caster.png').convert_alpha()
    hand_shooting_sprite = pygame.image.load('assets/textures/caster2.png').convert_alpha()
    bullet_image = pygame.image.load('assets/textures/bullet.png').convert_alpha()
    enemy_image = pygame.image.load('assets/textures/enemy.png').convert_alpha()  # Ensure this image is in the correct location
    medikit_image = pygame.image.load('assets/textures/medikit.png').convert_alpha()
    speedup_image = pygame.image.load('assets/textures/speedup.png').convert_alpha()
    
    hand_sprite = pygame.transform.scale(hand_sprite, (450, 450))  # Further enlarge the sprite
    hand_shooting_sprite = pygame.transform.scale(hand_shooting_sprite, (450, 450))  # Further enlarge the shooting sprite
    bullet_image = pygame.transform.scale(bullet_image, (40, 40))  # Increase the bullet size
    enemy_image = pygame.transform.scale(enemy_image, (TILE_SIZE // 2, TILE_SIZE // 2))  # Adjust enemy size to fit better in corridors
    medikit_image = pygame.transform.scale(medikit_image, (TILE_SIZE // 2, TILE_SIZE // 2))
    speedup_image = pygame.transform.scale(speedup_image, (TILE_SIZE // 2, TILE_SIZE // 2))

    projectiles = []
    enemies = []
    pickups = []

    for _ in range(5):  # Spawn multiple enemies at random positions on the map
        while True:
            x = random.randint(0, len(game_map[0]) - 1) * TILE_SIZE
            y = random.randint(0, len(game_map) - 1) * TILE_SIZE
            if game_map[y // TILE_SIZE][x // TILE_SIZE] != '#':
                enemies.append(Enemy(x, y, enemy_image))
                break
    
    for _ in range(2):  # Spawn medikits
        while True:
            x = random.randint(0, len(game_map[0]) - 1) * TILE_SIZE
            y = random.randint(0, len(game_map) - 1) * TILE_SIZE
            if game_map[y // TILE_SIZE][x // TILE_SIZE] != '#':
                pickups.append(Pickup(x, y, medikit_image, 'medikit'))
                break
    
    for _ in range(2):  # Spawn speedups
        while True:
            x = random.randint(0, len(game_map[0]) - 1) * TILE_SIZE
            y = random.randint(0, len(game_map) - 1) * TILE_SIZE
            if game_map[y // TILE_SIZE][x // TILE_SIZE] != '#':
                pickups.append(Pickup(x, y, speedup_image, 'speedup'))
                break

    shooting = False
    shooting_duration = 0.1  # Duration for displaying the shooting sprite
    shooting_timer = 0

    bobbing_amplitude = 5  # Amplitude of the bobbing motion
    bobbing_frequency = 0.1  # Frequency of the bobbing motion
    bobbing_phase = 0

    while True:
        dt = clock.tick(FPS) / 1000  # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Calculate the tip of the finger position
                    finger_tip_x = player.x + math.cos(player.angle) * 50  # Adjust the offset as needed
                    finger_tip_y = player.y + math.sin(player.angle) * 50
                    # Shoot a projectile
                    projectiles.append(Projectile(finger_tip_x, finger_tip_y, player.angle, bullet_image))
                    shooting = True
                    shooting_timer = shooting_duration
                    print(f"Shot fired: {len(projectiles)} projectiles in the air")

        player.movement()
        screen.fill(BLACK)
        ray_casting(screen, player, game_map, wall_texture, enemies, projectiles, pickups)  # Pass enemies and projectiles to raycasting

        # Update and draw projectiles
        for projectile in projectiles:
            projectile.update(dt, game_map, enemies)
            projectile.draw(screen)
            print(f"Projectile position: ({projectile.x}, {projectile.y}) Active: {projectile.active}")
        projectiles = [p for p in projectiles if p.active]

        # Update enemies
        for enemy in enemies:
            enemy.update(player.x, player.y, game_map)
            if enemy.rect.colliderect(player.x, player.y, TILE_SIZE, TILE_SIZE):
                player.take_damage(20)  # Takes 20 damage (1 hit)

        # Update pickups
        for pickup in pickups:
            if pickup.rect.colliderect(player.x, player.y, TILE_SIZE, TILE_SIZE):
                if pickup.type == 'medikit':
                    player.heal(40)  # Heals 40 health (2 hits)
                elif pickup.type == 'speedup':
                    player.speed_up()
                pickups.remove(pickup)

        # Update bobbing phase
        if any(pygame.key.get_pressed()):  # If any key is pressed, bob faster
            bobbing_phase += bobbing_frequency * 2
        else:  # If idle, bob slower
            bobbing_phase += bobbing_frequency

        bobbing_offset = math.sin(bobbing_phase) * bobbing_amplitude

        # Draw the hand sprite with bobbing effect
        if shooting:
            hand_sprite_rect = hand_shooting_sprite.get_rect(bottomright=(SCREEN_WIDTH, SCREEN_HEIGHT - bobbing_offset))
            screen.blit(hand_shooting_sprite, hand_sprite_rect)
            shooting_timer -= dt
            if shooting_timer <= 0:
                shooting = False
        else:
            hand_sprite_rect = hand_sprite.get_rect(bottomright=(SCREEN_WIDTH, SCREEN_HEIGHT - bobbing_offset))
            screen.blit(hand_sprite, hand_sprite_rect)

        pygame.display.flip()

if __name__ == '__main__':
    main()
