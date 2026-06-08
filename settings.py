import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

import pygame
vec = pygame.math.Vector2

# Game
WIDTH = 1600
HEIGHT = 900
FPS = 60
TILESIZE = 32

# Player
PLAYER_HP = 100
PLAYER_SPEED = 8
PLAYER_SIZE = 0.35
PLAYER_IMAGE = 'player/0.png'
PLAYER_HIT_RECT = pygame.Rect(0,0,35,35)

PL_START_X = 0
PL_START_Y = 0
GUN_OFFSET_X = 45
GUN_OFFSET_Y = 20


# Bullet settings
SHOOT_COOLDOWN = 20
BULLET_SCALE = 1.4
BULLET_SPEED = 50
BULLET_LIFETIME = 750

BULLET_IMAGE = 'bullet/1.png'
weapons = {
    'pistol': {'bullet_speed': 50,
               "bullet_scale": 1.4,
               "shoot_cooldown": 20,
               'bullet_lifetime': 750,
               'damage': 10}
    
}

# Enemy Settings
ENEMY_SPEED = 4
MONSTERS = {
    'necromancer': {'image': 'necromancer/necro.png', 
                    'speed': 5, 
                    'hitRect': pygame.Rect(0,0,30,30), 
                    'health': 20,
                    'dectection_radius': 400,
                    'attack_dmg': 20,
                    'avoid_rad': 50
                    }
}


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Items
ITEM_IMAGES = {'medkit': 'items/medKit.png',
               'box': 'items/supplyBox.png'}
HEALTH_PACK_RECOVERY = 20
BOBBING_RANGE = 10
BOBBING_SPEED = 0.3