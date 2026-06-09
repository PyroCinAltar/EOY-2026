import pygame
import math

from settings import WIDTH, HEIGHT, FPS, BULLET_DAMAGE, PLAYER_HP
from sprites import Player, Bullet, Enemy
from tilemap import TileMap

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# exit 
exit_active = False


# Load map
game_map = TileMap("map/spaceship.tmx")


class Camera:
    def __init__(self, width, height):
        self.offset = pygame.Vector2(0, 0)
        self.width = width
        self.height = height

    def update(self, target_rect):
        # Center camera on player
        self.offset.x += (target_rect.centerx - self.width // 2 - self.offset.x) * 0.1
        self.offset.y += (target_rect.centery - self.height // 2 - self.offset.y) * 0.1

# Player spawn
player = Player(*game_map.player_spawn)

# Enemies
enemies = [Enemy(x, y) for x, y in game_map.enemy_spawns]

bullets = []

cameraA = Camera(WIDTH, HEIGHT)

running = True

#exit
exit_active = False
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullets.append(
                Bullet(
                    player.rect.centerx,
                    player.rect.centery,
                    player.angle
                )
            )

    #checking if all enemies are dead then activating the exit
    if len(enemies) == 0:
        exit_active = True

    #draws the exit ig?
    if exit_active and game_map.exit_rect:
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            game_map.exit_rect.move(
                -cameraA.offset.x,
                -cameraA.offset.y
            )
        )
    
    #detects if player goes through exit
    if (
        exit_active
        and game_map.exit_rect
        and player.rect.colliderect(game_map.exit_rect)
    ):
        print("Level Complete!")

 

    keys = pygame.key.get_pressed()

    # Update
    player.move(keys, game_map.walls)
    player.update_angle(pygame.mouse.get_pos(), cameraA)

    for enemy in enemies:
        enemy.update(player, game_map.walls)
        enemy.attack(player)

    for bullet in bullets[:]:
        bullet.update()
        #bullet collision with wall check
        if bullet.hits_wall(game_map.walls):
            bullets.remove(bullet)
            continue
        
        if (
            bullet.rect.right < 0
            or bullet.rect.left > game_map.width
            or bullet.rect.bottom < 0
            or bullet.rect.top > game_map.height
        ):
            bullets.remove(bullet)

    # Bullet collisions
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.rect.colliderect(enemy.rect):
                enemy.hp -= BULLET_DAMAGE
                bullets.remove(bullet)

                if enemy.hp <= 0:
                    enemies.remove(enemy)
                break

    if player.hp <= 0:
        print("GAME OVER")
        running = False

    cameraA.update(player.rect)
    
    #rotation
    # player.move(keys, game_map.walls)
    # player.update_angle(cameraA)
        
    screen.fill((30, 30, 30))

    # HP bar background
    pygame.draw.rect(screen, (100, 100, 100), (20, 20, 200, 20))

    # HP bar fill
    hp_width = (player.hp / PLAYER_HP) * 200
    pygame.draw.rect(screen, (0, 255, 0), (20, 20, hp_width, 20))

    # Border
    pygame.draw.rect(screen, (255, 255, 255), (20, 20, 200, 20), 2)

    game_map.draw(screen, cameraA)

    player.draw(screen, cameraA)

    for enemy in enemies:
        enemy.draw(screen, cameraA)

    for bullet in bullets:
        bullet.draw(screen, cameraA)
    pygame.display.flip()

    

pygame.quit()