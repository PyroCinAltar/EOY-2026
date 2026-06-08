import pygame
from random import uniform, choice, randint, random
import math
import settings
from settings import *
from tilemap import collide_hit_rect
import pytweening
from itertools import chain
vec = pygame.math.Vector2

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y
            
            

# Player
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        # self.image = pygame.transform.rotozoom(pygame.image.load('player/0.png').convert_alpha(), 0, PLAYER_SIZE)
        # self.pos = pygame.math.Vector2(PL_START_X, PL_START_Y)
        # self.speed = PLAYER_SPEED
        # self.base_player_image = self.image
        # self.hitbox_rect = self.base_player_image.get_rect(center = self.pos)
        # self.rect = self.hitbox_rect.copy()
        # self.gun_barrel_offset = pygame.math.Vector2(GUN_OFFSET_X, GUN_OFFSET_Y)
        
        
        
        self.health = PLAYER_HP
        
        #shooting
        self.shoot_cooldown = 0
        self.shoot = False
    
    def player_rotation(self):
        self.mouse_coords = pygame.mouse.get_pos()
        self.x_change_mouse_player = (self.mouse_coords[0]-WIDTH//2)
        self.y_change_mouse_player =(self.mouse_coords[1]-HEIGHT//2)
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
        if pygame.mouse.get_pressed()[0]:
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot = False
    
    def is_shooting(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            spawn_bullet_pos = self.pos + self.gun_barrel_offset.rotate(self.angle)
            self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle)
            bullet_group.add(self.bullet)
            all_sprites_group.add(self.bullet)
            
    def take_damage(self, value):
        if ui.currentHP > 0:
            ui.currentHP -= value
            self.health -= value
        
        if ui.currentHP <= 0:
            ui.currentHP = 0
            self.health = 0
            
    def gain_health(self, value):
        if ui.currentHP < ui.maxHP:
            ui.currentHP += value
            self.health += value
            
        if ui.currentHP >= ui.maxHP:
            ui.currentHP = ui.maxHP
            self.health = ui.maxHP
           
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

# Projectile
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
        self.bullet_lifetime = BULLET_LIFETIME
        self.spawn_time = pygame.time.get_ticks() # gets the specific time the bullet was created
        pass
    
    def bullet_movement(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()
        pass
    def update(self):
        self.bullet_movement()
        
# Enemy 
class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(enemy_group, all_sprites_group)
        self.image = pygame.image.load('necromancer/0-3.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 2)
        
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.health = 4
        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.speed = ENEMY_SPEED
        # self.health = ENEMY_HEALTH
        self.attack_cooldown = 0
        self.position = pygame.math.Vector2(position)
        
    def take_damage(self):
        self.health -= PLAYER_ATTACK_DMG
        pass
        
    def hunt_player(self):
        player_vector = pygame.math.Vector2(player.hitbox_rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        distance = self.get_vector_distance(player_vector, enemy_vector)
        
        if distance > 0:
            self.direction = (player_vector - enemy_vector).normalize()
        else:
            self.direction = pygame.math.Vector2()
        
        self.velocity = self.direction * self.speed
        self.position += self.velocity
        
        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y
        
    def get_vector_distance(self, vect1, vect2):
        return(vect1-vect2).magnitude()
    
    def update(self):
        self.hunt_player()

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.rect.colliderect(player.hitbox_rect):
            if self.attack_cooldown == 0:
                self.attack()
                self.attack_cooldown = 60

        if self.health <= 0:
            self.kill()
        
class Necromancer(Enemy):
    def __init__(self, position):
        super().__init__(position)

        self.image = pygame.image.load(
            'necromancer/0-3.png'
        ).convert_alpha()

        self.image = pygame.transform.rotozoom(
            self.image, 0, 2
        )

        self.rect = self.image.get_rect(center=position)

        self.health = NECROMANCER_HP
        
    def attack(self):
        player.take_damage(NECROMANCER_ATTACK_DMG)
        