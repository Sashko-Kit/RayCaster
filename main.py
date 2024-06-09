import pygame
import math
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, TILE_SIZE, MAP_SIZE
from player import Player
from raycasting import ray_casting
from map import game_map
from projectile import Projectile, Flame
from enemy import Enemy
from pickup import Pickup

def setup_level():
    player = Player()

    wall_texture = pygame.image.load('assets/textures/wall.png').convert()
    hand_sprite = pygame.image.load('assets/textures/caster.png').convert_alpha()
    hand_shooting_sprite = pygame.image.load('assets/textures/caster2.png').convert_alpha()
    bullet_image = pygame.image.load('assets/textures/bullet.png').convert_alpha()
    enemy_image = pygame.image.load('assets/textures/enemy.png').convert_alpha()
    medikit_image = pygame.image.load('assets/textures/medikit.png').convert_alpha()
    speedup_image = pygame.image.load('assets/textures/speedup.png').convert_alpha()
    flame_image = pygame.image.load('assets/textures/flames.png').convert_alpha()
    flamethrower_image = pygame.image.load('assets/textures/flamethrower.png').convert_alpha()
    flamethrower_shooting_image = pygame.image.load('assets/textures/flamethrower2.png').convert_alpha()

    hand_sprite = pygame.transform.scale(hand_sprite, (450, 450))
    hand_shooting_sprite = pygame.transform.scale(hand_shooting_sprite, (450, 450))
    bullet_image = pygame.transform.scale(bullet_image, (40, 40))
    enemy_image = pygame.transform.scale(enemy_image, (TILE_SIZE // 2, TILE_SIZE // 2))
    medikit_image = pygame.transform.scale(medikit_image, (TILE_SIZE // 4, TILE_SIZE // 4))
    speedup_image = pygame.transform.scale(speedup_image, (TILE_SIZE // 4, TILE_SIZE // 4))
    flame_image = pygame.transform.scale(flame_image, (20, 20))
    flamethrower_image = pygame.transform.scale(flamethrower_image, (450, 450))
    flamethrower_shooting_image = pygame.transform.scale(flamethrower_shooting_image, (450, 450))

    projectiles = []
    enemies = []
    pickups = []

    for _ in range(5):
        while True:
            x = random.randint(0, len(game_map[0]) - 1) * TILE_SIZE
            y = random.randint(0, len(game_map) - 1) * TILE_SIZE
            if game_map[y // TILE_SIZE][x // TILE_SIZE] != '#':
                enemies.append(Enemy(x, y, enemy_image))
                break

    for _ in range(2):
        while True:
            x = random.randint(0, len(game_map[0]) - 1) * TILE_SIZE
            y = random.randint(0, len(game_map) - 1) * TILE_SIZE
            if game_map[y // TILE_SIZE][x // TILE_SIZE] != '#':
                pickups.append(Pickup(x, y, medikit_image, 'medikit'))
                break

    for _ in range(2):
        while True:
            x = random.randint(0, len(game_map[0]) - 1) * TILE_SIZE
            y = random.randint(0, len(game_map) - 1) * TILE_SIZE
            if game_map[y // TILE_SIZE][x // TILE_SIZE] != '#':
                pickups.append(Pickup(x, y, speedup_image, 'speedup'))
                break

    while True:
        x = random.randint(0, len(game_map[0]) - 1) * TILE_SIZE
        y = random.randint(0, len(game_map) - 1) * TILE_SIZE
        if game_map[y // TILE_SIZE][x // TILE_SIZE] != '#':
            pickups.append(Pickup(x, y, flamethrower_image, 'flamethrower'))
            break

    return player, wall_texture, hand_sprite, hand_shooting_sprite, bullet_image, enemy_image, medikit_image, speedup_image, flame_image, flamethrower_image, flamethrower_shooting_image, projectiles, enemies, pickups

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 55)
    player, wall_texture, hand_sprite, hand_shooting_sprite, bullet_image, enemy_image, medikit_image, speedup_image, flame_image, flamethrower_image, flamethrower_shooting_image, projectiles, enemies, pickups = setup_level()

    bobbing_phase = 0
    bobbing_frequency = 0.05
    bobbing_amplitude = 10
    damage_timer = 0
    shooting = False
    shooting_duration = 0.2
    shooting_timer = 0
    score = 0
    game_over = False

    def draw_text(text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect(center=(x, y))
        surface.blit(textobj, textrect)

    while True:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    if player.weapon == 'hand':
                        finger_tip_x = player.x + math.cos(player.angle) * 50
                        finger_tip_y = player.y + math.sin(player.angle) * 50
                        projectiles.append(Projectile(finger_tip_x, finger_tip_y, player.angle, bullet_image))
                        shooting = True
                        shooting_timer = shooting_duration
                        print(f"Shot fired: {len(projectiles)} projectiles in the air")
                    elif player.weapon == 'flamethrower':
                        shooting = True
                if event.key == pygame.K_r:
                    player, wall_texture, hand_sprite, hand_shooting_sprite, bullet_image, enemy_image, medikit_image, speedup_image, flame_image, flamethrower_image, flamethrower_shooting_image, projectiles, enemies, pickups = setup_level()
                    bobbing_phase = 0
                    damage_timer = 0
                    shooting = False
                    shooting_timer = 0
                    score = 0
                    game_over = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and player.weapon == 'flamethrower':
                    shooting = False

        if not game_over:
            player.movement()
            screen.fill(BLACK)
            ray_casting(screen, player, game_map, wall_texture, enemies, projectiles, pickups)

            for projectile in projectiles:
                projectile.update(dt, game_map, enemies)
            projectiles = [p for p in projectiles if p.active]

            for enemy in enemies:
                enemy.update(player.x, player.y, game_map)
                if enemy.rect.colliderect(player.rect) and damage_timer <= 0:
                    player.take_damage(20)
                    damage_timer = 2
                if enemy.health <= 0:
                    enemies.remove(enemy)
                    score += 10

            for pickup in pickups:
                if pickup.rect.colliderect(player.rect):
                    if pickup.type == 'medikit':
                        player.health = min(100, player.health + 40)
                    elif pickup.type == 'speedup':
                        player.speed *= 1.5
                    elif pickup.type == 'flamethrower':
                        player.weapon = 'flamethrower'
                    pickups.remove(pickup)

            if damage_timer > 0:
                damage_timer -= dt

            if any(pygame.key.get_pressed()):
                bobbing_phase += bobbing_frequency * 2
            else:
                bobbing_phase += bobbing_frequency

            bobbing_offset = math.sin(bobbing_phase) * bobbing_amplitude

            if shooting:
                if player.weapon == 'hand':
                    hand_sprite_rect = hand_shooting_sprite.get_rect(bottomright=(SCREEN_WIDTH, SCREEN_HEIGHT - bobbing_offset))
                    screen.blit(hand_shooting_sprite, hand_sprite_rect)
                    shooting_timer -= dt
                    if shooting_timer <= 0:
                        shooting = False
                elif player.weapon == 'flamethrower':
                    hand_sprite_rect = flamethrower_shooting_image.get_rect(bottomright=(SCREEN_WIDTH, SCREEN_HEIGHT - bobbing_offset))
                    screen.blit(flamethrower_shooting_image, hand_sprite_rect)
                    flame_x = player.x + math.cos(player.angle) * 50
                    flame_y = player.y + math.sin(player.angle) * 50
                    projectiles.append(Flame(flame_x, flame_y, player.angle, flame_image))
            else:
                if player.weapon == 'hand':
                    hand_sprite_rect = hand_sprite.get_rect(bottomright=(SCREEN_WIDTH, SCREEN_HEIGHT - bobbing_offset))
                    screen.blit(hand_sprite, hand_sprite_rect)
                elif player.weapon == 'flamethrower':
                    hand_sprite_rect = flamethrower_image.get_rect(bottomright=(SCREEN_WIDTH, SCREEN_HEIGHT - bobbing_offset))
                    screen.blit(flamethrower_image, hand_sprite_rect)

            draw_text(f'Score: {score}', font, (255, 255, 255), screen, SCREEN_WIDTH - 100, 50)

            if player.health <= 0:
                game_over = True

        else:
            draw_text('You Died', font, (255, 0, 0), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            draw_text('Press R to Restart', font, (255, 255, 255), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)

        pygame.display.flip()

if __name__ == '__main__':
    main()
