import pygame
import sys

# Initialize all Pygame modules
pygame.init()

# Setup window parameters (size and title)
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint - Practice 10")

# Define color constants in RGB format
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# State variables for UI and tools
colors = [BLACK, RED, GREEN, BLUE]
current_color = BLACK
tools = ['brush', 'rect', 'circle', 'eraser']
current_tool = 'brush'
brush_size = 5
eraser_size = 20

# Create a separate surface (canvas) to save the drawing.
# This is necessary so the drawing is not cleared when the screen updates.
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# Setup font for the UI
font = pygame.font.SysFont("Verdana", 16)

# Variables to track the drawing process for shapes
drawing = False
start_pos = (0, 0)

def draw_ui():
    """Handles the rendering of the top tool panel and buttons."""
    # Draw the panel background
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 60))
    
    # Draw color selection buttons
    for i, color in enumerate(colors):
        rect = pygame.Rect(10 + i * 45, 10, 40, 40)
        pygame.draw.rect(screen, color, rect)
        
        # Outline the active color (if the eraser is not selected)
        if color == current_color and current_tool != 'eraser':
            pygame.draw.rect(screen, WHITE, rect, 3)
            pygame.draw.rect(screen, BLACK, rect, 1)

    # Draw text for tool selection
    ui_texts = [
        ("Brush", 200, 'brush'),
        ("Rect", 270, 'rect'),
        ("Circle", 330, 'circle'),
        ("Eraser", 400, 'eraser')
    ]
    
    for text, x, tool_name in ui_texts:
        # Highlight the active tool in red
        text_color = RED if current_tool == tool_name else BLACK
        label = font.render(text, True, text_color)
        screen.blit(label, (x, 20))

# Main program loop
running = True
while running:
    # Render the canvas content onto the main screen
    screen.blit(canvas, (0, 0))
    
    mouse_pos = pygame.mouse.get_pos()
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Check for left mouse button click
                if mouse_pos[1] < 60:
                    # Handle clicks in the UI area (Y < 60)
                    
                    # Check for color button clicks
                    for i, color in enumerate(colors):
                        if 10 + i * 45 <= mouse_pos[0] <= 50 + i * 45:
                            current_color = color
                            if current_tool == 'eraser':
                                current_tool = 'brush' # Switch from eraser to brush when a color is selected
                    
                    # Check for tool text clicks
                    if 190 <= mouse_pos[0] <= 250: current_tool = 'brush'
                    elif 260 <= mouse_pos[0] <= 310: current_tool = 'rect'
                    elif 320 <= mouse_pos[0] <= 380: current_tool = 'circle'
                    elif 390 <= mouse_pos[0] <= 460: current_tool = 'eraser'
                else:
                    # Start drawing a shape in the workspace
                    drawing = True
                    start_pos = mouse_pos
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False
                # Finalize the shape onto the canvas surface upon releasing the button
                if current_tool == 'rect':
                    rect = pygame.Rect(start_pos[0], start_pos[1], mouse_pos[0] - start_pos[0], mouse_pos[1] - start_pos[1])
                    rect.normalize() # Normalize coordinates for correct rendering in any direction
                    pygame.draw.rect(canvas, current_color, rect, 2)
                elif current_tool == 'circle':
                    # Calculate the radius using the Pythagorean theorem based on the start and end points
                    radius = int(((mouse_pos[0] - start_pos[0])**2 + (mouse_pos[1] - start_pos[1])**2)**0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)
                    
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                # Continuous drawing for the brush and eraser (directly onto the canvas)
                if current_tool == 'brush':
                    pygame.draw.circle(canvas, current_color, event.pos, brush_size)
                elif current_tool == 'eraser':
                    pygame.draw.circle(canvas, WHITE, event.pos, eraser_size)

    # Preview shapes on the 'screen' rather than the 'canvas'
    # This allows seeing the shape outline while dragging the mouse
    if drawing:
        if current_tool == 'rect':
            temp_rect = pygame.Rect(start_pos[0], start_pos[1], mouse_pos[0] - start_pos[0], mouse_pos[1] - start_pos[1])
            temp_rect.normalize()
            pygame.draw.rect(screen, current_color, temp_rect, 2)
        elif current_tool == 'circle':
            radius = int(((mouse_pos[0] - start_pos[0])**2 + (mouse_pos[1] - start_pos[1])**2)**0.5)
            pygame.draw.circle(screen, current_color, start_pos, radius, 2)

    # Render the UI on top of all other elements
    draw_ui()
    
    # Update the screen
    pygame.display.flip()

# Exit the program
pygame.quit()
sys.exit()