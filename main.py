import pygame as pg
import sys
from random import choice, random
from os import path
from settings import *
from sprites2 import *
from tilemap import *

def draw_player_health(surface, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surface, col, fill_rect)
    pg.draw.rect(surface, WHITE, outline_rect, 2)
    
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Top Down Shooter")
        self.clock = pg.time.Clock()
        self.load_data()
    
    # Adding Text
    def draw_text(self, text, font_name, size, color, x, y, align='topleft'):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)
        
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.map_folder = path.join(game_folder, 'map')
        self.player_image = pg.image.load(path.join(img_folder, PLAYER_IMAGE)).convert_alpha()
        self.bullet_image = pg.image.load(path.join(img_folder, BULLET_IMAGE)).convert_alpha()
        self.enemy_image = pg.image.load(path.join(img_folder, MONSTERS['necromancer']['image'])).convert_alpha()
        
    
    def new_game(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder, '/Spaceship.tmx'))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'zombie':
                Enemy(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Barrier(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name in ['health', 'box']:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.night = False
        self.effects_sounds['level_start'].play()


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        # pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # game over?
        if len(self.mobs) == 0:
            self.playing = False
        # player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HP:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_RECOVERY)
            if hit.type == 'shotgun':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'shotgun'
                
                
        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for enemy in hits:
            if isinstance(enemy, Enemy):
                
                self.player.health -= MONSTERS[enemy.type]['attack_dmg']
                hit.vel = vec(0, 0)
                if self.player.health <= 0:
                    self.playing = False
                
                
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            hit.health -= weapons[self.player.weapon]['damage'] * len(hits[hit])
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = vec(0, 0)
    
    
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 100, RED,
                       WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("Press a key to start", self.title_font, 75, WHITE,
                       WIDTH / 2, HEIGHT * 3 / 4, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new_game()
    g.run()
    g.show_go_screen()