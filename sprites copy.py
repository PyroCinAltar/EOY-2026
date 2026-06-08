import pygame as pg
from random import uniform, choice, randint, random
import math
import settings
from settings import *
from tilemap import collide_hit_rect
import pytweening as tween
vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y
            
            

# Player
class Player(pg.sprite.Sprite):
    
    def __init__(self, game, x, y):
        super().__init__()
        # self.image = pygame.transform.rotozoom(pygame.image.load('player/0.png').convert_alpha(), 0, PLAYER_SIZE)
        # self.pos = pygame.math.Vector2(PL_START_X, PL_START_Y)
        # self.speed = PLAYER_SPEED
        # self.base_player_image = self.image
        # self.hitbox_rect = self.base_player_image.get_rect(center = self.pos)
        # self.rect = self.hitbox_rect.copy()
        # self.gun_barrel_offset = pygame.math.Vector2(GUN_OFFSET_X, GUN_OFFSET_Y)
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HP
        self.weapon = 'pistol'
        self.damaged = False
        
        #shooting
        self.shoot_cooldown = 0
        self.shoot = False
    
    def player_rotation(self):
        self.mouse_coords = pg.mouse.get_pos()
        self.x_change_mouse_player = (self.mouse_coords[0]-WIDTH//2)
        self.y_change_mouse_player =(self.mouse_coords[1]-HEIGHT//2)
        self.angle = math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player))
        self.image = pg.transform.rotate(self.base_player_image, -self.angle)
        self.rect = self.image.get_rect(center = self.hitbox_rect.center)
    
    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Movement
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.velocity_y = -self.speed
        if keys[pg.K_s]:
            self.velocity_y = self.speed
        if keys[pg.K_d]:
            self.velocity_x = self.speed
        if keys[pg.K_a]:
            self.velocity_x = -self.speed
            
        if self.velocity_x !=0 and self.velocity_y != 0:
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)
        
        # Shooting
        self.mouse_coords = pg.mouse.get_pos()
        if pg.mouse.get_pressed()[0]:
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot = False
            
    
    def is_shooting(self):
        if self.shoot_cooldown == 0:
           spawn_bullet_pos = self.vec_pos + self.gun_barrel_offset.rotate(self.angle)
           self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle)
           self.shoot_cooldown = weapons[self.weapon]['shoot_cooldown']
            
    def change_health(self, value):
        self.health += value
        if self.health > PLAYER_HP:
            self.health = PLAYER_HP
           
    def move(self):
        self.pos += pg.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center
        
    def update(self):
        self.user_input()
        self.move()
        self.player_rotation()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1



# Projectile
class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage):
        super().__init__()
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_images[weapons[game.player.weapon]['bullet_size']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * weapons[game.player.weapon]['bullet_speed'] * uniform(0.9, 1.1)
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage
    
    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > weapons[self.game.player.weapon]['bullet_lifetime']:
            self.kill()
        
# Enemy 
class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y, monster):
        super().__init__()
        self.type = monster
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MONSTERS[monster]['hitRect'].copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MONSTERS[monster]['health']
        self.speed = MONSTERS[monster]['speed']
        self.target = game.player
        
    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < MONSTERS[self.monster]['avoid_rad']:
                    self.acc += dist.normalize()
                    
                    
    def update(self):
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < MONSTERS[self.monster]['dectection_radius']**2:
            if random() < 0.002:
                choice(self.game.zombie_moan_sounds).play()
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        if self.health <= 0:
            choice(self.game.zombie_hit_sounds).play()
            self.kill()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))
            
    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MONSTERS[self.monster]['health'])
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MONSTERS[self.monster]['health']:
            pg.draw.rect(self.image, col, self.health_bar)


        
    # def hunt_player(self):
    #     player_vector = pg.math.Vector2(player.hitbox_rect.center)
    #     enemy_vector = pg.math.Vector2(self.rect.center)
    #     distance = self.get_vector_distance(player_vector, enemy_vector)
        
    #     if distance > 0:
    #         self.direction = (player_vector - enemy_vector).normalize()
    #     else:
    #         self.direction = pg.math.Vector2()
        
    #     self.velocity = self.direction * self.speed
    #     self.position += self.velocity
        
    #     self.rect.centerx = self.position.x
    #     self.rect.centery = self.position.y
        
    # def get_vector_distance(self, vect1, vect2):
    #     return(vect1-vect2).magnitude()
    
    # def update(self):
    #     self.hunt_player()

    #     if self.attack_cooldown > 0:
    #         self.attack_cooldown -= 1

    #     if self.rect.colliderect(player.hitbox_rect):
    #         if self.attack_cooldown == 0:
    #             self.attack()
    #             self.attack_cooldown = 60

    #     if self.health <= 0:
    #         self.kill()

class Item(pg.sprite.Sprite):

    def __init__(self, game, pos, type):
        super().__init__()
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1
        
    def update(self):
        # bobbing motion
        offset = BOBBING_RANGE * (self.tween(self.step / BOBBING_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOBBING_SPEED
        if self.step > BOBBING_RANGE:
            self.step = 0
            self.dir *= -1
            
class Barrier(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y