import pygame
from settings import *
import settings
import math
import sys    

pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('player/0.png').convert_alpha(), 0, PLAYER_SIZE)
        self.pos = pygame.math.Vector2(PL_START_X, PL_START_Y)
        self.speed = PLAYER_SPEED
        self.base_player_image = self.image
        self.hitbox_rect = self.base_player_image.get_rect(center = self.pos) # actually a hurtbox but ok
        self.rect = self.hitbox_rect.copy()
        
        #shooting
        self.shoot_cooldown = 0
        self.shoot = False
    
    def player_rotation(self):
        self.mouse_coords = pygame.mouse.get_pos()
        self.x_change_mouse_player = (self.mouse_coords[0]-self.hitbox_rect.centerx)
        self.y_change_mouse_player =(self.mouse_coords[1]-self.hitbox_rect.centery)
        self.angle = math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player))
        self.image = pygame.transform.rotate(self.base_player_image, -self.angle)
        self.rect = self.image.get_rect(center = self.hitbox_rect.center)
    
    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if keys[pygame.K_s]:
            self.velocity_y = self.speed
        if keys[pygame.K_d]:
            self.velocity_x = self.speed
        if keys[pygame.K_a]:
            self.velocity_x = -self.speed
            
        if self.velocity_x !=0 and self.velocity_y != 0:
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)
            
        
        # Shooting
        self.mouse_coords = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed() == (1, 0,(self.mouse_coords[0]-self.hitbox_rect.centerx), 0):
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot = False
    def is_shooting(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            spawn_bullet_pos = self.pos
            self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle)
            bullet_group.add(self.bullet)
            all_sprites_group.add(self.bullet)
            
           
    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center
        
    def update(self):
        self.user_input()
        self.move()
        self.player_rotation()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
            
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.image.load("bullet/1.png").convert()
        self.image = pygame.transform.rotozoom(self.image, 0, BULLET_SCALE)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = BULLET_SPEED
        self.x_vel = math.cos(self.angle * (2*math.pi/360)) * self.speed
        self.y_vel = math.sin(self.angle * (2*math.pi/360)) * self.speed
        pass
    
    def bullet_movement(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        pass
    def update(self):
        self.bullet_movement()
        
    
        
# class Camera(pygame.sprite.Group):
#     def __init__(self):
#         super().__init__() 
#         self.offset = pygame.math.Vector2()
            
if __name__ == "__main__":
    
    player = Player()
    
    all_sprites_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    
    all_sprites_group.add(player)
    
    
    while True:
        screen.fill((0,0,0))  
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        
        # screen.blit(player.image, player.rect) 
        # player.update()
        
        all_sprites_group.draw(screen)
        all_sprites_group.update()
        # pygame.draw.rect(screen, "red", player.hitbox_rect, width = 2)
        # pygame.draw.rect(screen, "yellow", player.rect, width = 2)
                
        pygame.display.update()
        clock.tick(FPS)