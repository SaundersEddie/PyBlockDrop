import pygame

class Button:
    def __init__(self, rect, text, font, color, text_color=(255,255,255)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
        txt_surface = self.font.render(self.text, True, self.text_color)
        txt_rect = txt_surface.get_rect(center=self.rect.center)
        surface.blit(txt_surface, txt_rect)

    def is_hover(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

def draw_modal(surface, font, text, close_text="Close"):
    modal_w, modal_h = 600, 350
    surface_w, surface_h = surface.get_size()
    modal_rect = pygame.Rect(
        (surface_w - modal_w) // 2,
        (surface_h - modal_h) // 2,
        modal_w, modal_h
    )
    pygame.draw.rect(surface, (50, 50, 70), modal_rect, border_radius=18)
    pygame.draw.rect(surface, (200, 200, 240), modal_rect, 4, border_radius=18)

    # Word-wrap the modal text if needed
    lines = []
    for paragraph in text.split('\n'):
        words = paragraph.split(' ')
        line = ''
        for word in words:
            test_line = (line + ' ' + word).strip()
            if font.size(test_line)[0] > modal_w - 60:  # Padding for modal
                lines.append(line)
                line = word
            else:
                line = test_line
        lines.append(line)

    # Render modal text
    y_offset = modal_rect.y + 40
    for line in lines:
        txt_surface = font.render(line, True, (255, 255, 255))
        txt_rect = txt_surface.get_rect(centerx=modal_rect.centerx, y=y_offset)
        surface.blit(txt_surface, txt_rect)
        y_offset += font.get_height() + 8

    # Close button - smaller, more visually like a button
    close_w, close_h = 140, 48
    close_rect = pygame.Rect(
        modal_rect.centerx - close_w // 2,
        modal_rect.bottom - close_h - 32,
        close_w,
        close_h
    )
    pygame.draw.rect(surface, (180, 80, 80), close_rect, border_radius=12)
    pygame.draw.rect(surface, (240, 220, 220), close_rect, 3, border_radius=12)
    close_surface = font.render(close_text, True, (255, 255, 255))
    close_rect_txt = close_surface.get_rect(center=close_rect.center)
    surface.blit(close_surface, close_rect_txt)
    return close_rect

