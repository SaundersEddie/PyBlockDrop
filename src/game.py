import os
import random
import pygame
from graphics import load_and_scale_piece_images

# --- GAME CONFIG ---
GRID_COLS = 10
GRID_ROWS = 20
BLOCK_SIZE = 48

_piece_images = None  # Cache for piece images

def discover_block_types(asset_dir="../assets/Graphics/Pieces"):
    # Only grab PNG files, drop the .png extension for piece name
    return [
        os.path.splitext(f)[0]
        for f in os.listdir(asset_dir)
        if f.lower().endswith(".png")
    ]

BLOCK_TYPES = discover_block_types()

def get_piece_images():
    global _piece_images
    if _piece_images is None:
        _piece_images = load_and_scale_piece_images("../assets/Graphics/Pieces", size=(BLOCK_SIZE, BLOCK_SIZE))
    return _piece_images

def start_new_grid(rows=GRID_ROWS, cols=GRID_COLS, fill_rows=3, block_types=None):
    if block_types is None:
        block_types = BLOCK_TYPES
    grid = [[None for _ in range(cols)] for _ in range(rows)]
    for r in range(rows - fill_rows, rows):
        for c in range(cols):
            if random.random() < 0.7:
                grid[r][c] = random.choice(block_types)
    return grid

def draw_game(screen, grid, current_piece=None):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    piece_images = get_piece_images()
    grid_width_px = cols * BLOCK_SIZE
    grid_height_px = rows * BLOCK_SIZE
    screen_width, screen_height = screen.get_size()
    offset_x = (screen_width - grid_width_px) // 2
    offset_y = (screen_height - grid_height_px) // 2

    # Draw grid
    for r in range(rows):
        for c in range(cols):
            block = grid[r][c]
            rect = pygame.Rect(offset_x + c * BLOCK_SIZE, offset_y + r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, (50, 50, 60), rect, border_radius=8)
            if block:
                img = piece_images.get(block)
                if img:
                    screen.blit(img, rect)

    # Draw the falling piece using y_pos for smooth animation
    if current_piece:
        block = current_piece["type"]
        col = current_piece["col"]
        y_pos = current_piece["y_pos"]
        # Only draw if within bounds and cell empty
        int_row = int(y_pos)
        if 0 <= int_row < rows and 0 <= col < cols and grid[int_row][col] is None:
            x_render = offset_x + col * BLOCK_SIZE
            y_render = offset_y + y_pos * BLOCK_SIZE
            img = piece_images.get(block)
            if img:
                screen.blit(img, (x_render, y_render))

def find_matches(grid, min_match=3):
    rows, cols = len(grid), len(grid[0])
    to_clear = set()

    # Horizontal check
    for r in range(rows):
        c = 0
        while c < cols:
            start = c
            while c + 1 < cols and grid[r][c] is not None and grid[r][c] == grid[r][c + 1]:
                c += 1
            if grid[r][start] is not None and c - start + 1 >= min_match:
                for clear_c in range(start, c + 1):
                    to_clear.add((r, clear_c))
            c += 1

    # Vertical check
    for c in range(cols):
        r = 0
        while r < rows:
            start = r
            while r + 1 < rows and grid[r][c] is not None and grid[r][c] == grid[r + 1][c]:
                r += 1
            if grid[start][c] is not None and r - start + 1 >= min_match:
                for clear_r in range(start, r + 1):
                    to_clear.add((clear_r, c))
            r += 1

    return to_clear

def clear_matches(grid, matches):
    for r, c in matches:
        grid[r][c] = None

def apply_gravity(grid):
    rows, cols = len(grid), len(grid[0])
    for c in range(cols):
        stack = [grid[r][c] for r in range(rows) if grid[r][c] is not None]
        # Fill from bottom up
        for r in range(rows - 1, -1, -1):
            if stack:
                grid[r][c] = stack.pop()
            else:
                grid[r][c] = None

