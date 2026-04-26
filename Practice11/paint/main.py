import pygame
import sys

# Initialize all Pygame modules
pygame.init()

# Setup window parameters (size and title)
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

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

# Added new tools to the list
tools = ['brush', 'rect', 'circle', 'eraser', 'square', 'right_tri', 'eq_tri', 'rhombus']
current_tool = 'brush'
brush_size = 5
eraser_size = 20

# Create a separate surface to save the drawing.
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# Setup font for the UI
font = pygame.font.SysFont("Verdana", 14) # Slightly smaller to fit all tools

# UI text labels and their starting X coordinates
ui_texts = [
    ("Brush", 200, 'brush'),
    ("Rect", 255, 'rect'),
    ("Square", 305, 'square'),
    ("Circle", 370, 'circle'),
    ("R.Tri", 425, 'right_tri'),
    ("E.Tri", 475, 'eq_tri'),
    ("Rhombus", 525, 'rhombus'),
    ("Eraser", 610, 'eraser')
]

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
    for text, x, tool_name in ui_texts:
        # Highlight the active tool in red
        text_color = RED if current_tool == tool_name else BLACK
        label = font.render(text, True, text_color)
        screen.blit(label, (x, 20))

def draw_shape(surface, tool, color, start, end):
    """Helper function to draw shapes on a given surface (screen for preview, canvas for final)."""
    if tool == 'rect':
        rect = pygame.Rect(start[0], start[1], end[0] - start[0], end[1] - start[1])
        rect.normalize()
        pygame.draw.rect(surface, color, rect, 2)
        
    elif tool == 'square':
        # Square logic: side length is the maximum of dx or dy
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        side = max(abs(dx), abs(dy))
        sign_x = 1 if dx >= 0 else -1
        sign_y = 1 if dy >= 0 else -1
        rect = pygame.Rect(start[0], start[1], side * sign_x, side * sign_y)
        rect.normalize()
        pygame.draw.rect(surface, color, rect, 2)
        
    elif tool == 'circle':
        # Calculate radius using Pythagorean theorem
        radius = int(((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5)
        pygame.draw.circle(surface, color, start, radius, 2)
        
    elif tool == 'right_tri':
        # Right Triangle: start point, bottom-left point, end point
        points = [start, (start[0], end[1]), end]
        pygame.draw.polygon(surface, color, points, 2)
        
    elif tool == 'eq_tri':
        # Equilateral/Isosceles Triangle fitting the bounding box
        points = [
            ((start[0] + end[0]) / 2, start[1]), # Top center
            (start[0], end[1]),                  # Bottom left
            (end[0], end[1])                     # Bottom right
        ]
        pygame.draw.polygon(surface, color, points, 2)
        
    elif tool == 'rhombus':
        # Rhombus fitting the bounding box
        points = [
            ((start[0] + end[0]) / 2, start[1]),             # Top center
            (end[0], (start[1] + end[1]) / 2),               # Right center
            ((start[0] + end[0]) / 2, end[1]),               # Bottom center
            (start[0], (start[1] + end[1]) / 2)              # Left center
        ]
        pygame.draw.polygon(surface, color, points, 2)

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
            if event.button == 1: # Left mouse button
                if mouse_pos[1] < 60:
                    # UI AREA CLICK HANDLING
                    
                    # 1. Color button clicks
                    for i, color in enumerate(colors):
                        if 10 + i * 45 <= mouse_pos[0] <= 50 + i * 45:
                            current_color = color
                            if current_tool == 'eraser':
                                current_tool = 'brush'
                    
                    # 2. Tool text clicks (Dynamic calculation using font width)
                    for text, x, tool_name in ui_texts:
                        text_width, text_height = font.size(text)
                        # Check if click is inside the text bounding box
                        if x <= mouse_pos[0] <= x + text_width and 20 <= mouse_pos[1] <= 20 + text_height:
                            current_tool = tool_name
                else:
                    # Start drawing a shape in the workspace
                    drawing = True
                    start_pos = mouse_pos
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False
                # Finalize the shape onto the permanent canvas
                draw_shape(canvas, current_tool, current_color, start_pos, mouse_pos)
                    
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                # Continuous drawing for brush and eraser directly on the canvas
                if current_tool == 'brush':
                    pygame.draw.circle(canvas, current_color, event.pos, brush_size)
                elif current_tool == 'eraser':
                    pygame.draw.circle(canvas, WHITE, event.pos, eraser_size)

    # Preview shapes on the 'screen' rather than the 'canvas'
    if drawing and current_tool not in ['brush', 'eraser']:
        draw_shape(screen, current_tool, current_color, start_pos, mouse_pos)

    # Render the UI on top of all other elements
    draw_ui()
    
    # Update the screen
    pygame.display.flip()

# Exit the program
pygame.quit()
sys.exit()