import pygame
import time
import random

# Initial game state variables
snake_speed = 15
window_x = 720
window_y = 480

# Define RGB color constants
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0) # Used for high-weight food

# Initialize Pygame and display window
pygame.init()
pygame.display.set_caption('Snake - Practice 11')
game_window = pygame.display.set_mode((window_x, window_y))

# Setup FPS controller
fps = pygame.time.Clock()

# Define initial snake layout
snake_position = [100, 50]
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]]

# Food state variables
food_position = []
food_color = white
food_weight = 10
food_spawn_time = 0
FOOD_LIFESPAN = 5000 # Time in milliseconds before food disappears (5 seconds)

def spawn_food():
    """Generates food at a random coordinate with randomized weights/colors and resets the timer."""
    global food_position, food_color, food_weight, food_spawn_time
    
    # Calculate random grid position
    food_position = [random.randrange(1, (window_x//10)) * 10, 
                     random.randrange(1, (window_y//10)) * 10]
    
    # Assign random weight and color (Practice 11 Task 2.1)
    weight_chance = random.randint(1, 100)
    if weight_chance <= 50:
        food_color = red
        food_weight = 10 # 50% chance for standard food
    elif weight_chance <= 85:
        food_color = blue
        food_weight = 20 # 35% chance for medium food
    else:
        food_color = yellow
        food_weight = 30 # 15% chance for high-value food
        
    # Record the timestamp of spawn for the disappearance timer
    food_spawn_time = pygame.time.get_ticks()

# Initial food spawn
spawn_food()

# Movement state
direction = 'RIGHT'
change_to = direction

# Player progression stats
score = 0
level = 1
foods_eaten = 0 # Tracks how many foods consumed to calculate level-ups

def show_stats(color, font, size):
    """Renders the current score and level on the screen."""
    stats_font = pygame.font.SysFont(font, size)
    # Combine score and level into a single string
    stats_surface = stats_font.render(f'Score: {score}   |   Level: {level}', True, color)
    stats_rect = stats_surface.get_rect()
    game_window.blit(stats_surface, stats_rect)

def game_over():
    """Handles the terminal state of the game, rendering the final score before exiting."""
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x/2, window_y/2)
    
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    
    time.sleep(2)
    pygame.quit()
    quit()

# Main Game Loop
while True:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Validate direction to prevent immediate self-collision (cannot reverse directly)
    if change_to == 'UP' and direction != 'DOWN': direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP': direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT': direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT': direction = 'RIGHT'

    # Update snake head position
    if direction == 'UP': snake_position[1] -= 10
    if direction == 'DOWN': snake_position[1] += 10
    if direction == 'LEFT': snake_position[0] -= 10
    if direction == 'RIGHT': snake_position[0] += 10

    # 2. Logic: Food Timer (Practice 11 Task 2.2)
    current_time = pygame.time.get_ticks()
    if current_time - food_spawn_time > FOOD_LIFESPAN:
        spawn_food() # Timer expired, respawn food elsewhere

    # 3. Logic: Collision & Growth
    snake_body.insert(0, list(snake_position))
    
    # Check if snake head aligns with food coordinates
    if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
        score += food_weight
        foods_eaten += 1
        
        # Level up mechanics: every 4 foods eaten, increase level and speed
        if foods_eaten % 4 == 0:
            level += 1
            snake_speed += 2 # Game runs faster
            
        spawn_food() # Generate new food
    else:
        # If no food eaten, remove tail to maintain length
        snake_body.pop()
        
    # 4. Rendering
    game_window.fill(black)
    
    # Draw snake body
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
        
    # Draw food using its assigned color
    pygame.draw.rect(game_window, food_color, pygame.Rect(food_position[0], food_position[1], 10, 10))

    # 5. Collision Checks (Game Over triggers)
    # Check boundary collision
    if snake_position[0] < 0 or snake_position[0] > window_x-10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y-10:
        game_over()

    # Check self-collision
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # Render UI statistics
    show_stats(white, 'times new roman', 20)

    # Refresh display buffer
    pygame.display.update()

    # Throttle loop to match snake speed (FPS)
    fps.tick(snake_speed)