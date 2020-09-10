import time
import random as rnd
import math
import pygame
import glob
import os
from player import Player
from bullet import Bullet

def write_score(last_score):
    is_highscore = False
    if not os.path.exists("highscores.txt"):
        g = open("highscores.txt", "w")
        for x in range(10):
            g.write("0\n")
        g.close()

    new_score_data = []
    with open("highscores.txt", "r") as f:  # f는 연 파일 오브젝트
        score_data = f.readlines()

        cindex = 0
        while cindex < len(score_data):
            score = score_data[cindex].strip("\n")
            if last_score > float(score):
                is_highscore = True
                new_score_data.append(f"{last_score}\n")
                for x in range(cindex, len(score_data)-1):
                    new_score_data.append(f"{score_data[x].strip()}\n")
                break
            else:
                new_score_data.append(f"{score}\n")
            cindex += 1

    with open("highscores.txt", "w") as f:
        f.writelines(new_score_data)

    return is_highscore

def collision(player_obj, bullet_obj):
    if math.sqrt((player_obj.pos[0] - bullet_obj.pos[0]) ** 2 + 
                 (player_obj.pos[1] - bullet_obj.pos[1]) ** 2) < bullet_obj.radius + 5:
        return True
    return False

def draw_text(txt, size, pos, color):
    font = pygame.font.Font('freesansbold.ttf', size)
    r = font.render(txt, True, color)
    screen.blit(r, pos)

# Initialize the pygame
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
WIDTH, HEIGHT = 1000, 800

explosion_images = []  # list of explosion_gif image frames
explosion_index = 0  # index to play gif frames in game loop
for img in glob.glob("explosion_gif/*.png"):
    g = pygame.image.load(img)
    g.set_colorkey((0,0,0))  # set black color to be transparent
    explosion_images.append(g)

# Background image
bg_image = pygame.image.load('bg.jpg')

# Background music
pygame.mixer.Channel(0).play(pygame.mixer.Sound('bgm.wav'), loops=-1)

pygame.display.set_caption("총알 피하기")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
FPS=60

player = Player(WIDTH/2, HEIGHT/2)

bullets = []
for i in range(10):
    size = rnd.randint(7, 20)
    bullets.append(Bullet(0, rnd.random()*HEIGHT, size, (size * 5) % player.maxlives/3,   rnd.random()-0.5, rnd.random()-0.5))

time_for_adding_bullets = 0

start_time = time.time()

bg_pos = 0
bg_dt = -0.01

# set invulnerability time(in seconds)
INVULNERABILITY_TIME = 2 * FPS  # time for invulnerability after hit
invul_tick = 0  # current invulnerability tick 
DRAW_PLAYER = True  # is the player image being blitted?
in_highscores = False  # is final time in highscore?
#Game Loop
running = True
gameover = False
score = 0
while running:

    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #게임 창의 X버튼을 눌렀을 때
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.goto(-1,0)
            elif event.key == pygame.K_RIGHT:
                player.goto(1,0)
            elif event.key == pygame.K_UP:
                player.goto(0,-1)
            elif event.key == pygame.K_DOWN:
                player.goto(0,1)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.goto(1,0)
            elif event.key == pygame.K_RIGHT:
                player.goto(-1,0)
            elif event.key == pygame.K_UP:
                player.goto(0,1)
            elif event.key == pygame.K_DOWN:
                player.goto(0,-1)
        
    # 화면에 검은색 채우기 (RGB - Red, Green, Blue)
    # screen.fill((0, 0, 0))
    
    bg_pos += bg_dt * dt
    if bg_image.get_width() + bg_pos - WIDTH <= 0 or bg_pos >= 0: bg_dt *= -1
    screen.blit(bg_image, (int(bg_pos), 0))

    player.update(dt, screen)
    for b in bullets:
        b.update_and_draw(dt, screen)

    pygame.draw.rect(screen, (255, 0, 0), [10, 50, 200, 40])
    if player.lives > 0:
        pygame.draw.rect(screen, (0, 255, 0), [10, 50, int(200 * player.lives / 100), 40])
    draw_text(f"HP: {round(player.lives, 2)}", 32, (10, 100), (255,255,255))

    if gameover:
        draw_text("GAME OVER", 100, (WIDTH/2 - 300, HEIGHT/2 - 50), (255,255,255))
        txt = "Time: {:.1f}  Bullets: {}".format(score, len(bullets))
        if in_highscores:
            draw_text(txt, 32, (int(WIDTH/2) - 150, int(HEIGHT/2) + 50), (255,0,0))
        else:
            draw_text(txt, 32, (int(WIDTH/2) - 150, int(HEIGHT/2) + 50), (255,255,255))
        if explosion_index < len(explosion_images):
            screen.blit(explosion_images[explosion_index], (player.pos[0] - 175, player.pos[1] - 175))
            explosion_index += 1
    else:
        score = time.time() - start_time
        txt = "Time: {:.1f}  Bullets: {}".format(score, len(bullets))
        draw_text(txt, 32, (10, 10), (255,255,255))
   
    if not gameover:
        if DRAW_PLAYER:
            player.draw(screen)
        if invul_tick == 0:
            for b in bullets:
                if collision(player, b):
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('bullet_hit.wav'), loops=1)
                    player.lives -= b.damage
                    player.lives = 0 if player.lives < 0 else player.lives
                    invul_tick = INVULNERABILITY_TIME
                    if player.lives <= 0:
                        gameover = True
                        in_highscores = write_score(score)
                    #time.sleep(2)
                    #running = False
            DRAW_PLAYER = True
        elif invul_tick > 0:
            if invul_tick % 5 == 0 and invul_tick != 0:  # make player image blink while invulnerable
                DRAW_PLAYER = not DRAW_PLAYER

            invul_tick -= 1

        time_for_adding_bullets += dt
        if time_for_adding_bullets > 1000:
            size = rnd.randint(7, 20)
            bullets.append(Bullet(0, rnd.random()*HEIGHT, size, (size * 5) % player.maxlives/3,   rnd.random()-0.5, rnd.random()-0.5))
            time_for_adding_bullets -= 1000
    
    pygame.display.update() #화면에 새로운 그림을 그린다 (화면을 갱신한다)