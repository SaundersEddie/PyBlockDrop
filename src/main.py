import pygame
import sys
from graphics import load_and_scale_piece_images, load_font
from ui import Button, draw_modal
from game import start_new_grid, draw_game, GRID_COLS, BLOCK_TYPES

def main():
    pygame.init()
    WIDTH, HEIGHT = 1920, 1080
    CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PyBlockDrop")

    font_path = "../assets/Fonts/Kenney Future.ttf"
    title_font = load_font(font_path, 96)
    button_font = load_font(font_path, 48)
    modal_font = load_font(font_path, 24)

    button_width, button_height = 400, 80
    button_spacing = 40
    labels = ["Play", "About", "Options"]
    buttons = []
    for i, label in enumerate(labels):
        total_height = (button_height + button_spacing) * len(labels)
        y_offset = i * (button_height + button_spacing)
        btn_x = CENTER_X - button_width // 2
        btn_y = CENTER_Y - total_height // 2 + y_offset
        buttons.append(
            Button((btn_x, btn_y, button_width, button_height), label, button_font, (80, 120, 200))
        )

    about_modal = False
    options_modal = False

    STATE_MENU = "menu"
    STATE_GAME = "game"
    current_state = STATE_MENU

    grid = []
    current_piece = None

    running = True
    clock = pygame.time.Clock()
    while running:
        screen.fill((30, 30, 40))

        if current_state == STATE_MENU:
            title_surface = title_font.render("PyBlockDrop", True, (220, 180, 40))
            title_rect = title_surface.get_rect(center=(CENTER_X, CENTER_Y - 250))
            screen.blit(title_surface, title_rect)

            for btn in buttons:
                btn.draw(screen)

            close_button_rect = None
            if about_modal:
                close_button_rect = draw_modal(
                    screen, modal_font, "PyBlockDrop\n\nBy Mr. YT\n\nMatch-3 falling block puzzle.\nNo ads. Just fun."
                )
            elif options_modal:
                close_button_rect = draw_modal(
                    screen, modal_font, "Options Coming Soon!"
                )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if about_modal or options_modal:
                        if close_button_rect and close_button_rect.collidepoint((mx, my)):
                            about_modal = False
                            options_modal = False
                    else:
                        if buttons[0].is_hover((mx, my)):
                            grid = start_new_grid()
                            current_piece = {
                                "type": BLOCK_TYPES[pygame.time.get_ticks() % len(BLOCK_TYPES)],  # A little variety
                                "row": 0,
                                "col": GRID_COLS // 2
                            }
                            current_state = STATE_GAME
                        elif buttons[1].is_hover((mx, my)):
                            about_modal = True
                        elif buttons[2].is_hover((mx, my)):
                            options_modal = True

        elif current_state == STATE_GAME:
            draw_game(screen, grid, current_piece)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if current_piece:
                        row = current_piece["row"]
                        col = current_piece["col"]
                        # Move left
                        if event.key == pygame.K_LEFT:
                            new_col = col - 1
                            if new_col >= 0 and grid[row][new_col] is None:
                                current_piece["col"] = new_col
                        # Move right
                        elif event.key == pygame.K_RIGHT:
                            new_col = col + 1
                            if new_col < GRID_COLS and grid[row][new_col] is None:
                                current_piece["col"] = new_col
                    # ESC to return to menu (optional)
                    if event.key == pygame.K_ESCAPE:
                        current_state = STATE_MENU

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
