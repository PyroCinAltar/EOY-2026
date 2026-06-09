import pygame
import math

from settings import WIDTH, HEIGHT, FPS, BULLET_DAMAGE, PLAYER_HP, MAX_NAME_LENGTH
from sprites import Player, Bullet, Enemy
from tilemap import TileMap
from database import init_db, add_score, get_top_scores

init_db()
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# exit 
exit_active = False

# timer
start_time = 0
final_time = 0

start_time = pygame.time.get_ticks()
current_time = (pygame.time.get_ticks() - start_time) / 1000

# Input
player_name = ""
typing_name = False

show_leaderboard = False


# Load map
game_map = TileMap("map/spaceship.tmx")

# Game states
GAME_STATE_MENU = "menu"
GAME_STATE_PLAYING = "playing"
GAME_STATE_GAME_OVER = "game_over"
GAME_STATE_COMPLETE = "complete"

game_state = GAME_STATE_MENU

def draw_text(screen, text, size, x, y, color=(255,255,255)):
    font = pygame.font.SysFont(None, size)
    img = font.render(text, True, color)
    screen.blit(img, (x, y))
    
def draw_menu(screen):
    screen.fill((20, 20, 20))
    draw_text(screen, "TOP DOWN SHOOTER", 64, 250, 200)
    draw_text(screen, "Press ENTER to Start", 36, 320, 320)
    
def draw_game_over(screen):
    screen.fill((0, 0, 0))
    draw_text(screen, "GAME OVER", 64, 350, 250, (255, 0, 0))
    draw_text(screen, "Press R to Restart", 36, 330, 350)
    
def draw_complete(screen):
    screen.fill((0, 50, 0))

    draw_text(screen, "LEVEL COMPLETE!", 64, 280, 200, (0,255,0))
    draw_text(screen, f"Time: {final_time:.2f}s", 36, 380, 280)

    if typing_name:
        draw_text(screen, "Enter Name:", 36, 420, 340)
        draw_text(screen, player_name, 36, 420, 380)
        
def draw_leaderboard(screen, scores):
    screen.fill((10, 10, 10))

    draw_text(screen, "TOP 10 SCORES", 50, 350, 80)

    y = 160
    for i, (name, time) in enumerate(scores):
        draw_text(screen, f"{i+1}. {name} - {time:.2f}s", 36, 320, y)
        y += 40
    
class Camera:
    def __init__(self, width, height):
        self.offset = pygame.Vector2(0, 0)
        self.width = width
        self.height = height

    def update(self, target_rect):
        # Center camera on player
        self.offset.x += (target_rect.centerx - self.width // 2 - self.offset.x) * 0.1
        self.offset.y += (target_rect.centery - self.height // 2 - self.offset.y) * 0.1
        

def reset_game():
    global player, enemies, bullets, game_map, cameraA, exit_active

    game_map = TileMap("map/spaceship.tmx")
    player = Player(*game_map.player_spawn)
    enemies = [Enemy(x, y) for x, y in game_map.enemy_spawns]
    bullets = []
    cameraA = Camera(WIDTH, HEIGHT)
    exit_active = False
    
def handle_name_input(event, name):
    if event.key == pygame.K_BACKSPACE:
        return name[:-1]

    if event.key == pygame.K_RETURN:
        return name

    # only allow letters and space
    if event.unicode.isalpha() or event.unicode == " ":
        if len(name) < MAX_NAME_LENGTH:
            return name + event.unicode

    return name



    

# Player spawn
player = Player(*game_map.player_spawn)

# Enemies
enemies = [Enemy(x, y) for x, y in game_map.enemy_spawns]

bullets = []

cameraA = Camera(WIDTH, HEIGHT)

running = True

#exit
exit_active = False

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == GAME_STATE_MENU:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = GAME_STATE_PLAYING

        elif game_state in (GAME_STATE_GAME_OVER, GAME_STATE_COMPLETE):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()
                game_state = GAME_STATE_MENU
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullets.append(
                Bullet(
                    player.rect.centerx,
                    player.rect.centery,
                    player.angle
                )
            )

    screen.fill((30, 30, 30))

    if game_state == GAME_STATE_MENU:
        draw_menu(screen)

    elif game_state == GAME_STATE_PLAYING:
        screen.fill((30, 30, 30))

        if game_state == GAME_STATE_MENU:
            draw_menu(screen)

        elif game_state == GAME_STATE_PLAYING:

            # EVERYTHING YOU ALREADY HAVE GOES HERE:
            keys = pygame.key.get_pressed()

            player.move(keys, game_map.walls)
            player.update_angle(pygame.mouse.get_pos(), cameraA)

            for enemy in enemies:
                enemy.update(player, game_map.walls)
                enemy.attack(player)

            for bullet in bullets[:]:
                bullet.update()

                if bullet.hits_wall(game_map.walls):
                    bullets.remove(bullet)
                    continue

                if (bullet.rect.right < 0 or bullet.rect.left > game_map.width or
                    bullet.rect.bottom < 0 or bullet.rect.top > game_map.height):
                    bullets.remove(bullet)

            for bullet in bullets[:]:
                for enemy in enemies[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.hp -= BULLET_DAMAGE
                        bullets.remove(bullet)

                        if enemy.hp <= 0:
                            enemies.remove(enemy)
                        break

            cameraA.update(player.rect)

            # EXIT CHECK
            if len(enemies) == 0:
                exit_active = True

            #draws the exit ig?
            if exit_active and game_map.exit_rect:
                pygame.draw.rect(
                    screen,
                    (0, 255, 0),
                        game_map.exit_rect.move(
                            -cameraA.offset.x,
                            -cameraA.offset.y
                        )
                    )
                
                #detects if player goes through exit
                if (
                    exit_active
                    and game_map.exit_rect
                    and player.rect.colliderect(game_map.exit_rect)
                ):
                    final_time = (pygame.time.get_ticks() - start_time) / 1000
                    game_state = GAME_STATE_COMPLETE
                    typing_name = True
                    player_name = ""        


            if player.hp <= 0:
                game_state = GAME_STATE_GAME_OVER

            # DRAW GAME WORLD
            game_map.draw(screen, cameraA)
            player.draw(screen, cameraA)

            for enemy in enemies:
                enemy.draw(screen, cameraA)

            for bullet in bullets:
                bullet.draw(screen, cameraA)

            # UI
            pygame.draw.rect(screen, (100,100,100), (20,20,200,20))
            hp_width = (player.hp / PLAYER_HP) * 200
            pygame.draw.rect(screen, (0,255,0), (20,20,hp_width,20))
            pygame.draw.rect(screen, (255,255,255), (20,20,200,20), 2)

    elif game_state == GAME_STATE_GAME_OVER:
        draw_game_over(screen)

    elif game_state == GAME_STATE_COMPLETE:
        draw_complete(screen)
            
    if game_state == GAME_STATE_COMPLETE and typing_name:

        if event.type == pygame.KEYDOWN:

            # ENTER → confirm name
            if event.key == pygame.K_RETURN:
                if player_name == "":
                    player_name = "PLAYER"

                add_score(player_name.strip().upper(), final_time)
                typing_name = False
                leaderboard = get_top_scores()
                show_leaderboard = True

            # BACKSPACE → delete
            elif event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]

            # LETTER INPUT ONLY
            else:
                if len(player_name) < MAX_NAME_LENGTH:
                    if event.unicode.isalpha() or event.unicode == " ":
                        player_name += event.unicode
                
    elif show_leaderboard:
        draw_leaderboard(screen, leaderboard)
        
    
    pygame.display.flip()

    

pygame.quit()