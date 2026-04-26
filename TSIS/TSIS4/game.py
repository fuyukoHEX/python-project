import pygame, random
from config import *

snake = [(100,100)]
dx, dy = CELL, 0

food = (200,200)
poison = (300,300)

power = None
power_pos = None
power_time = 0
active_power = None

score = 0
level = 1
speed = 10

obstacles = []


def new_pos():
    return (
        random.randrange(0, WIDTH, CELL),
        random.randrange(0, HEIGHT, CELL)
    )


def reset():
    global snake, dx, dy, score, level, speed, obstacles
    snake = [(100,100)]
    dx, dy = CELL, 0
    score = 0
    level = 1
    speed = 10
    obstacles = []


def make_obstacles():
    global obstacles
    obstacles = []
    for _ in range(level * 3):
        obstacles.append(new_pos())


def update():
    global food, poison, power, power_pos, power_time
    global active_power, score, level, speed

    head = (snake[0][0] + dx, snake[0][1] + dy)

    # collision
    if head in snake or head in obstacles:
        if active_power == "shield":
            active_power = None
        else:
            return "gameover"

    if not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT):
        if active_power == "shield":
            active_power = None
        else:
            return "gameover"

    snake.insert(0, head)

    # food
    if head == food:
        score += 1
        food = new_pos()

        if score % 5 == 0:
            level += 1
            speed += 1
            if level >= 3:
                make_obstacles()
    else:
        snake.pop()

    # poison
    if head == poison:
        if len(snake) > 1: snake.pop()
        if len(snake) > 1: snake.pop()
        if len(snake) <= 1:
            return "gameover"
        poison = new_pos()

    # power spawn
    if not power:
        power = random.choice(["speed", "slow", "shield"])
        power_pos = new_pos()
        power_time = pygame.time.get_ticks()

    # pickup
    if power and head == power_pos:
        active_power = power
        power = None
        power_time = pygame.time.get_ticks()

    # effects
    if active_power == "speed":
        speed = 15
    elif active_power == "slow":
        speed = 5

    if active_power and pygame.time.get_ticks() - power_time > 5000:
        active_power = None
        speed = 10 + level

    return "game"


def draw(screen, settings, bg):
    screen.blit(bg, (0,0))

    # grid
    if settings["grid"]:
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(screen, GRAY, (x,0),(x,HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(screen, GRAY, (0,y),(WIDTH,y))

    # snake
    for s in snake:
        pygame.draw.rect(screen, settings["snake_color"], (*s,CELL,CELL))

    pygame.draw.rect(screen, GREEN, (*food,CELL,CELL))
    pygame.draw.rect(screen, DARK_RED, (*poison,CELL,CELL))

    if power:
        pygame.draw.rect(screen, BLUE, (*power_pos,CELL,CELL))

    for o in obstacles:
        pygame.draw.rect(screen, RED, (*o,CELL,CELL))