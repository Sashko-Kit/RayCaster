import pygame
import math
from settings import *

def ray_casting(screen, player, game_map, wall_texture, enemies, projectiles, pickups):
    ox, oy = player.x, player.y
    map_size = MAP_SIZE * TILE_SIZE
    cur_angle = player.angle - FOV / 2
    texture_width = wall_texture.get_width()
    texture_height = wall_texture.get_height()
    
    # Prepare a list to hold depths for rendering enemies correctly
    wall_depths = [float('inf')] * NUM_RAYS
    
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        for depth in range(1, MAX_DEPTH):  # start from 1 to avoid division by zero
            x = ox + depth * cos_a
            y = oy + depth * sin_a
            if 0 < x < map_size and 0 < y < map_size:
                map_x, map_y = int(x / TILE_SIZE), int(y / TILE_SIZE)
                if game_map[map_y][map_x] == '#':
                    depth *= math.cos(player.angle - cur_angle)
                    proj_height = PROJ_COEFF / depth
                    
                    # Texture coordinates
                    texture_x = int((x % TILE_SIZE) / TILE_SIZE * texture_width) if sin_a > 0 else int((y % TILE_SIZE) / TILE_SIZE * texture_width)
                    wall_column = wall_texture.subsurface(texture_x, 0, 1, texture_height)
                    wall_column = pygame.transform.scale(wall_column, (SCALE, int(proj_height)))
                    screen.blit(wall_column, (ray * SCALE, SCREEN_HEIGHT // 2 - int(proj_height) // 2))
                    wall_depths[ray] = depth  # Save the depth of this wall
                    break
        cur_angle += DELTA_ANGLE

    # Sort enemies by distance from the player
    sorted_enemies = sorted(enemies, key=lambda enemy: (enemy.x - ox) ** 2 + (enemy.y - oy) ** 2, reverse=True)

    # Render enemies
    for enemy in sorted_enemies:
        dx = enemy.x - ox
        dy = enemy.y - oy
        distance = math.sqrt(dx**2 + dy**2)
        angle = math.atan2(dy, dx) - player.angle

        if -FOV / 2 < angle < FOV / 2:
            depth = distance * math.cos(angle)
            proj_height = PROJ_COEFF / depth
            scale = proj_height / TILE_SIZE
            screen_x = (SCREEN_WIDTH // 2) + int((angle / DELTA_ANGLE) * SCALE)
            if 0 <= int(screen_x / SCALE) < NUM_RAYS and depth < wall_depths[int(screen_x / SCALE)]:
                enemy_image = pygame.transform.scale(enemy.image, (int(TILE_SIZE * scale), int(TILE_SIZE * scale)))
                screen.blit(enemy_image, (screen_x - enemy_image.get_width() // 2, SCREEN_HEIGHT // 2 - enemy_image.get_height() // 2))

    # Render projectiles
    for projectile in projectiles:
        if projectile.active:
            proj_x = projectile.x
            proj_y = projectile.y
            dx = proj_x - ox
            dy = proj_y - oy
            distance = math.sqrt(dx ** 2 + dy ** 2)
            angle = math.atan2(dy, dx) - player.angle

            if -FOV / 2 < angle < FOV / 2:
                depth = distance * math.cos(angle)
                proj_height = PROJ_COEFF / depth
                scale = proj_height / TILE_SIZE
                screen_x = (SCREEN_WIDTH // 2) + int((angle / DELTA_ANGLE) * SCALE)
                if 0 <= int(screen_x / SCALE) < NUM_RAYS and depth < wall_depths[int(screen_x / SCALE)]:
                    projectile_image = pygame.transform.scale(projectile.image, (int(TILE_SIZE * scale), int(TILE_SIZE * scale)))
                    screen.blit(projectile_image, (screen_x - projectile_image.get_width() // 2, SCREEN_HEIGHT // 2 - projectile_image.get_height() // 2))

    # Render pickups
    for pickup in pickups:
        dx = pickup.x - ox
        dy = pickup.y - oy
        distance = math.sqrt(dx**2 + dy**2)
        angle = math.atan2(dy, dx) - player.angle

        if -FOV / 2 < angle < FOV / 2:
            depth = distance * math.cos(angle)
            proj_height = PROJ_COEFF / depth
            scale = proj_height / TILE_SIZE
            screen_x = (SCREEN_WIDTH // 2) + int((angle / DELTA_ANGLE) * SCALE)
            if 0 <= int(screen_x / SCALE) < NUM_RAYS and depth < wall_depths[int(screen_x / SCALE)]:
                pickup_image = pygame.transform.scale(pickup.image, (int(TILE_SIZE * scale * 0.5), int(TILE_SIZE * scale * 0.5)))  # Smaller size
                screen.blit(pickup_image, (screen_x - pickup_image.get_width() // 2, SCREEN_HEIGHT // 2 - pickup_image.get_height() // 2))

    # Draw the minimap
    minimap_size = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 3
    cell_size = minimap_size / MAP_SIZE
    minimap_surface = pygame.Surface((minimap_size, minimap_size))
    minimap_surface.fill((50, 50, 50))
    for y, row in enumerate(game_map):
        for x, char in enumerate(row):
            if char == '#':
                pygame.draw.rect(minimap_surface, (255, 255, 255), (x * cell_size, y * cell_size, cell_size, cell_size))
    pygame.draw.circle(minimap_surface, (255, 0, 0), (int(player.x / TILE_SIZE * cell_size), int(player.y / TILE_SIZE * cell_size)), max(2, int(cell_size / 2)))
    
    # Draw the player's field of view on the minimap
    fov_left_angle = player.angle - FOV / 2
    fov_right_angle = player.angle + FOV / 2
    fov_left_x = player.x + 100 * math.cos(fov_left_angle)
    fov_left_y = player.y + 100 * math.sin(fov_left_angle)
    fov_right_x = player.x + 100 * math.cos(fov_right_angle)
    fov_right_y = player.y + 100 * math.sin(fov_right_angle)
    
    pygame.draw.line(minimap_surface, (0, 255, 0), (int(player.x / TILE_SIZE * cell_size), int(player.y / TILE_SIZE * cell_size)),
                     (int(fov_left_x / TILE_SIZE * cell_size), int(fov_left_y / TILE_SIZE * cell_size)), 2)
    pygame.draw.line(minimap_surface, (0, 255, 0), (int(player.x / TILE_SIZE * cell_size), int(player.y / TILE_SIZE * cell_size)),
                     (int(fov_right_x / TILE_SIZE * cell_size), int(fov_right_y / TILE_SIZE * cell_size)), 2)

    # Draw the enemies on the minimap
    for enemy in enemies:
        pygame.draw.circle(minimap_surface, (255, 0, 0), (int(enemy.x / TILE_SIZE * cell_size), int(enemy.y / TILE_SIZE * cell_size)), max(2, int(cell_size / 2)))

    # Draw the health bar
    health_bar_width = minimap_size
    health_bar_height = 20
    health_percentage = player.health / 100
    health_bar_surface = pygame.Surface((health_bar_width, health_bar_height))
    health_bar_surface.fill((100, 100, 100))
    pygame.draw.rect(health_bar_surface, (255, 0, 0), (0, 0, health_bar_width * health_percentage, health_bar_height))
    screen.blit(health_bar_surface, (10, SCREEN_HEIGHT - minimap_size - health_bar_height - 20))
    
    screen.blit(minimap_surface, (10, SCREEN_HEIGHT - minimap_size - 10))
