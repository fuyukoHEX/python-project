import pygame, sys
from pygame.locals import *
import random, time

# Initialize all Pygame modules
pygame.init()

# Frame rate settings
FPS = 60
FramePerSec = pygame.time.Clock()

# Color constants
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game configuration and state variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_SCORE = 0
COINS_TO_SPEED_UP = 10 # Threshold 'N' required to increase game speed

# Font setup
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load background and audio assets
background = pygame.image.load("AnimatedStreet.png")
pygame.mixer.music.load('background.wav') 
pygame.mixer.music.play(-1) # Play BGM on infinite loop

# Screen setup
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer - Practice 11")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        # Respawn enemy at the top when it leaves the screen bounds
        if (self.rect.top > SCREEN_HEIGHT):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # Restrict movement within left bound
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        # Restrict movement within right bound
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Keep the original image cached to avoid quality loss during repeated scaling
        self.original_image = pygame.image.load("coin.png").convert_alpha()
        self.reset()

    def move(self):
        self.rect.move_ip(0, SPEED)
        # Respawn coin if missed
        if (self.rect.top > SCREEN_HEIGHT):
            self.reset()
    
    def reset(self):
        """Randomizes the weight, scales the image, and resets the position."""
        # Generate random weight (1 to 3 points)
        self.weight = random.randint(1, 3)
        
        # Scale the coin dynamically: higher weight results in a larger sprite
        size = 20 + (self.weight * 10) 
        self.image = pygame.transform.scale(self.original_image, (size, size))
        
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Instantiate game objects
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Manage sprite groups for collision detection and rendering
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Main game loop
while True:
    # Event polling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw background layer
    DISPLAYSURF.blit(background, (0,0))
    
    # Draw UI overlays
    scores = font_small.render("Enemies: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))

    coin_text = font_small.render("Coins: " + str(COIN_SCORE), True, BLACK)
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 100, 10))

    # Move and render all entities
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Handle Coin Collision Logic
    if pygame.sprite.spritecollideany(P1, coins):
        old_score = COIN_SCORE
        COIN_SCORE += C1.weight # Add dynamic weight to total score
        
        # Calculate if the threshold 'N' has been crossed to increase speed
        if COIN_SCORE // COINS_TO_SPEED_UP > old_score // COINS_TO_SPEED_UP:
            SPEED += 1.0 
            
        C1.reset() # Immediately recycle the coin

    # Handle Enemy Collision Logic (Game Over State)
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.music.stop() 
          pygame.mixer.Sound('crash.wav').play()
          time.sleep(0.5)
                   
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
          
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          
          time.sleep(2)
          pygame.quit()
          sys.exit()        
        
    pygame.display.update()
    FramePerSec.tick(FPS)