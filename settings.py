# settings.py
import pygame

WIDTH = 1000
HEIGHT = 700
FPS = 60

PLAYER_SPEED = 4
BULLET_SPEED = 10

PLAYER_HP = 100
BULLET_DAMAGE = 1
TILE_SIZE = 32



# Enemy Settings
ENEMY_SPEED = 4
MONSTERS = {
    'necromancer': {'image': 'sprites/blob.png', 
                    'speed': 4, 
                    'hitRect': pygame.Rect(0,0,30,30), 
                    'health': 25,
                    'detection_radius': 500,
                    'attack_dmg': 20,
                    'avoid_rad': 50,
                    'cooldown': 1000
                
                    }
}

MAX_NAME_LENGTH = 12