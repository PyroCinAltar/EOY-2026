# Modules
import pygame
import math
import sys
import pytmx
from pytmx.util_pygame import load_pygame

# Files
from settings import *
from tilemap import *
from sprites import *


# Loading game
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top Down Shooter")
clock = pygame.time.Clock()

# background = pygame.image.load('floors/ground.png').convert()
background = load_pygame(os.path.join('map/Spaceship.tmx'))
font = pygame.font.SysFont('Library/font/Skia', 30)


class UI():
    def __init__(self):
        self.maxHP = 4
        self.currentHP = 4
        self.HP_bar_length = 4
        self.health_ratio = self.maxHP / self.HP_bar_length 
        self.bar_color = None
        self.bar_length = 100
    
    def display_health_bar(self): 
        pygame.draw.rect(screen, BLACK, (10, 15, self.bar_length * 3, 20)) 

        if self.currentHP >= 3:
            pygame.draw.rect(screen, GREEN, (10, 15, self.currentHP * 3, 20))  
            self.bar_color = GREEN
        elif self.currentHP >= 1:
            pygame.draw.rect(screen, YELLOW, (10, 15, self.currentHP * 3, 20)) 
            self.bar_color = YELLOW 
        elif self.currentHP >= 0:
            pygame.draw.rect(screen, RED, (10, 15, self.currentHP * 3, 20))
            self.bar_color = RED
        pygame.draw.rect(screen, WHITE, (10, 15, self.bar_length * 3, 20), 4)

            
    def display_health_text(self):
        health_surface = font.render(f"{player.health} / {self.maxHP}", False, self.bar_color) 
        health_rect = health_surface.get_rect(center = (410, 25))
        screen.blit(health_surface, health_rect)
            
    def update(self): 
        self.display_health_bar()
        self.display_health_text()



if __name__ == "__main__":
    
    all_sprites_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    
    
    while True:
        screen.fill((0,0,0))  
        
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        # map.draw_map(screen)
                
        
        # screen.blit(player.image, player.rect) 
        # player.update()
        
    
        all_sprites_group.draw(screen)
        # camera.custom_draw()
        all_sprites_group.update()
        for bullet in bullet_group:
            hit_enemies = pygame.sprite.spritecollide(
                bullet,
                enemy_group,
                False
            )
            for enemy in hit_enemies:
                enemy.take_damage()
                bullet.kill()
        UI.update()
        # pygame.draw.rect(screen, "red", player.hitbox_rect, width = 2)
        # pygame.draw.rect(screen, "yellow", player.rect, width = 2)
                
        pygame.display.update()
        clock.tick(FPS)