import pygame, json
import game
from config import *
from db import *

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

init_db()

# settings
with open("TSIS/TSIS4/settings.json") as f:
    settings = json.load(f)

# background image
bg = pygame.image.load("TSIS/TSIS4/assets/bg.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# music
if settings["sound"]:
    pygame.mixer.music.load("TSIS/TSIS4/assets/music.mp3")
    pygame.mixer.music.play(-1)

state = "menu"
username = ""

def text(t,x,y):
    screen.blit(font.render(t,True,WHITE),(x,y))

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        # MENU
        if state == "menu":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    game.reset()
                    state = "game"
                elif e.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += e.unicode

        # GAME
        if state == "game":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP: game.dx,game.dy=0,-CELL
                if e.key == pygame.K_DOWN: game.dx,game.dy=0,CELL
                if e.key == pygame.K_LEFT: game.dx,game.dy=-CELL,0
                if e.key == pygame.K_RIGHT: game.dx,game.dy=CELL,0

        # GAME OVER
        if state == "gameover":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    game.reset()
                    state = "game"
                if e.key == pygame.K_m:
                    state = "menu"
                if e.key == pygame.K_l:
                    state = "leaderboard"

        # LEADERBOARD
        if state == "leaderboard":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_m:
                    state = "menu"

    # MENU
    if state == "menu":
        screen.blit(bg,(0,0))
        text("ENTER NAME:",200,200)
        text(username,200,240)
        text("PRESS ENTER",200,300)

    # GAME
    elif state == "game":
        result = game.update()
        game.draw(screen, settings, bg)

        text(f"Score:{game.score}",10,10)
        text(f"Level:{game.level}",10,30)
        text(f"Best:{get_best(username)}",10,50)

        if result == "gameover":
            save_score(username, game.score, game.level)
            state = "gameover"

    # GAME OVER
    elif state == "gameover":
        screen.blit(bg,(0,0))
        text("GAME OVER",220,200)
        text("R - retry",220,250)
        text("M - menu",220,280)
        text("L - leaderboard",200,310)

    # LEADERBOARD
    elif state == "leaderboard":
        screen.blit(bg,(0,0))
        text("TOP 10",250,100)

        y = 150
        for i,s in enumerate(get_top()):
            text(f"{i+1}. {s[0]} - {s[1]}",200,y)
            y += 30

        text("M - menu",220,500)

    pygame.display.flip()
    clock.tick(game.speed)

pygame.quit()