import pygame
import sys
from datetime import datetime
from collections import deque

# ─── Init ────────────────────────────────────────────────────────────────────
pygame.init()

WIDTH, HEIGHT = 900, 650
TOOLBAR_H = 90          # two-row toolbar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint — TSIS 2")

# ─── Colors ───────────────────────────────────────────────────────────────────
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
RED    = (255, 0,   0)
GREEN  = (0,   200, 0)
BLUE   = (0,   0,   255)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
PURPLE = (150, 0,   200)
GRAY   = (210, 210, 210)
DGRAY  = (150, 150, 150)
ACCENT = (220, 50,  50)   # active-tool highlight

PALETTE = [BLACK, WHITE, RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE]

# ─── State ────────────────────────────────────────────────────────────────────
current_color = BLACK
current_tool  = 'brush'
brush_sizes   = [2, 5, 10]
size_index    = 1           # default = medium (5 px)

# Text-tool state
text_active   = False
text_pos      = (0, 0)
text_buffer   = ""

# Shape-drawing state
drawing   = False
start_pos = (0, 0)
prev_pos  = None            # for pencil line-between-points

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

font_ui   = pygame.font.SysFont("Verdana", 12)
font_text = pygame.font.SysFont("Arial", 20)

# ─── Tool list (row 1 & 2) ────────────────────────────────────────────────────
# Each entry: (label, tool_name, row, x_offset)
# We'll lay them out dynamically.
TOOLS_ROW1 = [
    ("Brush",   "brush"),
    ("Pencil",  "pencil"),
    ("Line",    "line"),
    ("Rect",    "rect"),
    ("Square",  "square"),
    ("Circle",  "circle"),
    ("R.Tri",   "right_tri"),
    ("E.Tri",   "eq_tri"),
    ("Rhombus", "rhombus"),
]
TOOLS_ROW2 = [
    ("Fill",    "fill"),
    ("Eraser",  "eraser"),
    ("Text",    "text"),
    ("S:Small", "size_s"),
    ("S:Med",   "size_m"),
    ("S:Large", "size_l"),
    ("Ctrl+S → Save", "save_hint"),   # visual label only, not clickable tool
]

# ─── Helpers ─────────────────────────────────────────────────────────────────

def brush_size():
    return brush_sizes[size_index]


def tool_rects_row(tool_list, y_start, x_start=4, gap=6):
    """Return list of (rect, tool_name) for a tool row."""
    x = x_start
    result = []
    for label, name in tool_list:
        w, _ = font_ui.size(label)
        w += 10
        rect = pygame.Rect(x, y_start, w, 22)
        result.append((rect, label, name))
        x += w + gap
    return result


row1_layout = tool_rects_row(TOOLS_ROW1, y_start=6)
row2_layout = tool_rects_row(TOOLS_ROW2, y_start=34)

# ─── UI drawing ───────────────────────────────────────────────────────────────

def draw_ui():
    global size_index
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_H))
    pygame.draw.line(screen, DGRAY, (0, TOOLBAR_H), (WIDTH, TOOLBAR_H), 1)

    # ── Tool buttons row 1
    for rect, label, name in row1_layout:
        active = (current_tool == name)
        col = ACCENT if active else DGRAY
        pygame.draw.rect(screen, col, rect, border_radius=4)
        tc = WHITE if active else BLACK
        surf = font_ui.render(label, True, tc)
        screen.blit(surf, (rect.x + 5, rect.y + 5))

    # ── Tool buttons row 2
    for rect, label, name in row2_layout:
        if name == "save_hint":
            surf = font_ui.render(label, True, DGRAY)
            screen.blit(surf, (rect.x, rect.y + 5))
            continue
        # size buttons highlight when that size is active
        if name == "size_s": active = (size_index == 0)
        elif name == "size_m": active = (size_index == 1)
        elif name == "size_l": active = (size_index == 2)
        else: active = (current_tool == name)
        col = ACCENT if active else DGRAY
        pygame.draw.rect(screen, col, rect, border_radius=4)
        tc = WHITE if active else BLACK
        surf = font_ui.render(label, True, tc)
        screen.blit(surf, (rect.x + 5, rect.y + 5))

    # ── Color palette (bottom strip of toolbar)
    py = TOOLBAR_H - 24
    for i, c in enumerate(PALETTE):
        r = pygame.Rect(4 + i * 28, py, 24, 18)
        pygame.draw.rect(screen, c, r)
        if c == current_color:
            pygame.draw.rect(screen, ACCENT, r, 2)
        else:
            pygame.draw.rect(screen, DGRAY, r, 1)

    # ── Active color preview
    pygame.draw.rect(screen, current_color, (240, py, 36, 18))
    pygame.draw.rect(screen, BLACK, (240, py, 36, 18), 1)
    lbl = font_ui.render("Color", True, BLACK)
    screen.blit(lbl, (280, py + 2))

    # ── Brush size indicator
    bx, by = 380, py + 9
    pygame.draw.circle(screen, BLACK, (bx, by), brush_size())
    lbl = font_ui.render(f"Size: {brush_size()}px", True, BLACK)
    screen.blit(lbl, (bx + 14, py + 2))

    # ── Text cursor hint
    if text_active:
        hint = font_ui.render(f'Typing: "{text_buffer}█"  Enter=OK  Esc=Cancel', True, ACCENT)
        screen.blit(hint, (460, py + 2))


# ─── Shape drawing ────────────────────────────────────────────────────────────

def draw_shape(surface, tool, color, start, end, lw=2):
    if tool == 'line':
        pygame.draw.line(surface, color, start, end, lw)

    elif tool == 'rect':
        r = pygame.Rect(start, (end[0]-start[0], end[1]-start[1]))
        r.normalize()
        pygame.draw.rect(surface, color, r, lw)

    elif tool == 'square':
        dx, dy = end[0]-start[0], end[1]-start[1]
        side = max(abs(dx), abs(dy))
        sx = 1 if dx >= 0 else -1
        sy = 1 if dy >= 0 else -1
        r = pygame.Rect(start, (side*sx, side*sy))
        r.normalize()
        pygame.draw.rect(surface, color, r, lw)

    elif tool == 'circle':
        radius = int(((end[0]-start[0])**2 + (end[1]-start[1])**2)**0.5)
        if radius > 0:
            pygame.draw.circle(surface, color, start, radius, lw)

    elif tool == 'right_tri':
        pts = [start, (start[0], end[1]), end]
        pygame.draw.polygon(surface, color, pts, lw)

    elif tool == 'eq_tri':
        pts = [((start[0]+end[0])//2, start[1]), (start[0], end[1]), (end[0], end[1])]
        pygame.draw.polygon(surface, color, pts, lw)

    elif tool == 'rhombus':
        mx, my = (start[0]+end[0])//2, (start[1]+end[1])//2
        pts = [(mx, start[1]), (end[0], my), (mx, end[1]), (start[0], my)]
        pygame.draw.polygon(surface, color, pts, lw)


# ─── Flood fill ───────────────────────────────────────────────────────────────

def flood_fill(surface, pos, fill_color):
    x, y = int(pos[0]), int(pos[1])
    if not surface.get_rect().collidepoint(x, y):
        return
    target_color = surface.get_at((x, y))[:3]
    if target_color == fill_color[:3]:
        return

    q = deque()
    q.append((x, y))
    visited = set()
    visited.add((x, y))

    sw, sh = surface.get_size()
    while q:
        cx, cy = q.popleft()
        if surface.get_at((cx, cy))[:3] != target_color:
            continue
        surface.set_at((cx, cy), fill_color)
        for nx, ny in ((cx-1,cy),(cx+1,cy),(cx,cy-1),(cx,cy+1)):
            if 0 <= nx < sw and 0 <= ny < sh and (nx,ny) not in visited:
                visited.add((nx,ny))
                q.append((nx,ny))


# ─── Save canvas ──────────────────────────────────────────────────────────────

def save_canvas():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"canvas_{ts}.png"
    pygame.image.save(canvas, fname)
    print(f"[Saved] {fname}")


# ─── Click handling helpers ────────────────────────────────────────────────────

def handle_toolbar_click(pos):
    """Process clicks inside the toolbar. Returns True if consumed."""
    global current_tool, current_color, size_index, text_active, text_buffer

    # Row 1 tools
    for rect, label, name in row1_layout:
        if rect.collidepoint(pos):
            current_tool = name
            text_active = False
            return True

    # Row 2 tools / size buttons
    for rect, label, name in row2_layout:
        if name == "save_hint":
            continue
        if rect.collidepoint(pos):
            if name == "size_s":   size_index = 0
            elif name == "size_m": size_index = 1
            elif name == "size_l": size_index = 2
            else:
                current_tool = name
                if name == "text":
                    text_active = False
                    text_buffer = ""
            return True

    # Palette
    py = TOOLBAR_H - 24
    for i, c in enumerate(PALETTE):
        r = pygame.Rect(4 + i*28, py, 24, 18)
        if r.collidepoint(pos):
            current_color = c
            if current_tool == 'eraser':
                current_tool = 'brush'
            return True

    return False


# ─── Main loop ────────────────────────────────────────────────────────────────
clock = pygame.time.Clock()
running = True

while running:
    screen.blit(canvas, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ── Keyboard ──────────────────────────────────────────────────────────
        elif event.type == pygame.KEYDOWN:

            # Text tool input
            if text_active:
                if event.key == pygame.K_RETURN:
                    # Commit text to canvas
                    surf = font_text.render(text_buffer, True, current_color)
                    canvas.blit(surf, text_pos)
                    text_active = False
                    text_buffer = ""
                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                    text_buffer = ""
                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]
                else:
                    if event.unicode and event.unicode.isprintable():
                        text_buffer += event.unicode
                continue  # don't process other shortcuts while typing

            # Ctrl+S — save
            mods = pygame.key.get_mods()
            if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                save_canvas()

            # Brush size shortcuts
            elif event.key == pygame.K_1:
                size_index = 0
            elif event.key == pygame.K_2:
                size_index = 1
            elif event.key == pygame.K_3:
                size_index = 2

        # ── Mouse button down ─────────────────────────────────────────────────
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            if pos[1] < TOOLBAR_H:
                handle_toolbar_click(pos)
            else:
                # ── Canvas area
                if current_tool == 'text':
                    text_active = True
                    text_pos = pos
                    text_buffer = ""
                elif current_tool == 'fill':
                    flood_fill(canvas, pos, current_color)
                else:
                    drawing  = True
                    start_pos = pos
                    prev_pos  = pos

        # ── Mouse button up ───────────────────────────────────────────────────
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if drawing:
                drawing = False
                if current_tool not in ('brush', 'pencil', 'eraser'):
                    draw_shape(canvas, current_tool, current_color,
                               start_pos, mouse_pos, brush_size())
            prev_pos = None

        # ── Mouse motion ──────────────────────────────────────────────────────
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                if current_tool == 'brush':
                    pygame.draw.circle(canvas, current_color, event.pos, brush_size())

                elif current_tool == 'pencil':
                    if prev_pos:
                        pygame.draw.line(canvas, current_color,
                                         prev_pos, event.pos, brush_size())
                    prev_pos = event.pos

                elif current_tool == 'eraser':
                    pygame.draw.circle(canvas, WHITE, event.pos, brush_size() * 3)

    # ── Live shape preview ────────────────────────────────────────────────────
    if drawing and current_tool not in ('brush', 'pencil', 'eraser'):
        draw_shape(screen, current_tool, current_color,
                   start_pos, mouse_pos, brush_size())

    # ── Live text preview ─────────────────────────────────────────────────────
    if text_active:
        preview = font_text.render(text_buffer + "█", True, current_color)
        screen.blit(preview, text_pos)

    draw_ui()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
