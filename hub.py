import pygame
from settings import *
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
        
        #shooting
        self.shoot_cooldown = 0
        self.shoot = False
    
    
    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.velocity_y = -self.speed
        
        
        #shooting
        if pygame.mouse.get_pressed() == (1, 0, 0):
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot = False
    def is_shooting(self):
        if self.shoot_cooldowm == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
    def update(self):
        self.user_input()
        # self.move()
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

if __name__ == "__main__":
    
    player = Player()
    
    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        screen.blit(player.image, player.pos) 
                
        pygame.display.update()
        clock.tick(FPS)