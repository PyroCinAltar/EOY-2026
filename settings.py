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
    'necromancer': {'image': 'necromancer/necro.png', 
                    'speed': 5, 
                    'hitRect': pygame.Rect(0,0,30,30), 
                    'health': 20,
                    'detection_radius': 200,
                    'attack_dmg': 20,
                    'avoid_rad': 50,
                    'cooldown': 1000
                
                    }
}