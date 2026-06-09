import pygame
import math
import random
from settings import PLAYER_SPEED, BULLET_SPEED, BULLET_DAMAGE, PLAYER_HP, MONSTERS

# ---------------- PLAYER ----------------

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.hp = PLAYER_HP
        self.angle = 0
        
    #rotating
    def update_angle(self, mouse_pos, camera):
        mx, my = mouse_pos

    # convert mouse into world space
        mx += camera.offset.x
        my += camera.offset.y

        dx = mx - self.rect.centerx
        dy = my - self.rect.centery

        self.angle = math.atan2(dy, dx)
    

    def move(self, keys, walls):
        dx = 0
        dy = 0

        if keys[pygame.K_w]: dy = -PLAYER_SPEED
        if keys[pygame.K_s]: dy = PLAYER_SPEED
        if keys[pygame.K_a]: dx = -PLAYER_SPEED
        if keys[pygame.K_d]: dx = PLAYER_SPEED
        
        length = math.hypot(dx, dy)

        if length != 0:
            dx /= length
            dy /= length

            dx *= PLAYER_SPEED
            dy *= PLAYER_SPEED

        # X collision
        self.rect.x += dx
        for w in walls:
            if self.rect.colliderect(w):
                if dx > 0: self.rect.right = w.left
                if dx < 0: self.rect.left = w.right

        # Y collision
        self.rect.y += dy
        for w in walls:
            if self.rect.colliderect(w):
                if dy > 0: self.rect.bottom = w.top
                if dy < 0: self.rect.top = w.bottom

    def draw(self, screen, camera):
        pygame.draw.rect(
            screen,
            (50, 120, 255),
            self.rect.move(-camera.offset.x, -camera.offset.y)
        )
        
        # Col-Hit Box
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            self.rect.move(-camera.offset.x, -camera.offset.y),
            2  # thickness = outline only
        )
        
        # Rotation Angle
        pos = self.rect.center
        pos = (pos[0] - camera.offset.x, pos[1] - camera.offset.y)

    # direction line
        end_x = pos[0] + math.cos(self.angle) * 20
        end_y = pos[1] + math.sin(self.angle) * 20

        pygame.draw.line(screen, (255, 255, 0), pos, (end_x, end_y), 2)
            


# ---------------- BULLET ----------------

class Bullet:
    def __init__(self, x, y, angle):
        self.rect = pygame.Rect(x, y, 6, 6)
        self.dx = math.cos(angle) * BULLET_SPEED
        self.dy = math.sin(angle) * BULLET_SPEED
        
        self.damage = BULLET_DAMAGE

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self, screen, camera):
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            self.rect.move(-camera.offset.x, -camera.offset.y)
        )
    
    #doesn't let bullets pass through walls
    def hits_wall(self, walls):
        for wall in walls:
            if self.rect.colliderect(wall):
                return True
        return False
        


# ---------------- ENEMY ----------------

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 28, 28)
        self.speed = 2
        self.hp = 3
        self.damage = MONSTERS['necromancer']['attack_dmg']
        self.last_attack = 0
        self.attack_cooldown = MONSTERS['necromancer']['cooldown']

    def update(self, player, walls):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)

        if dist != 0:
            move_x = dx / dist * self.speed
            move_y = dy / dist * self.speed

            # X movement
            self.rect.x += move_x

            for wall in walls:
                if self.rect.colliderect(wall):
                    if move_x > 0:
                        self.rect.right = wall.left
                    elif move_x < 0:
                        self.rect.left = wall.right

            # Y movement
            self.rect.y += move_y

            for wall in walls:
                if self.rect.colliderect(wall):
                    if move_y > 0:
                        self.rect.bottom = wall.top
                    elif move_y < 0:
                        self.rect.top = wall.bottom
                        
    def draw(self, screen, camera):
        pygame.draw.rect(
            screen,
            (220, 60, 60),
            self.rect.move(-camera.offset.x, -camera.offset.y)
        )
        
    def attack(self, player):
        current_time = pygame.time.get_ticks()

        if self.rect.colliderect(player.rect):
            if current_time - self.last_attack > self.attack_cooldown:
                player.hp -= self.damage
                self.last_attack = current_time

                print("Player HP:", player.hp)