import pygame
import os

def load_and_scale_piece_images(folder_path, size=(32, 32)):
    piece_images = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.png'):
            key = os.path.splitext(filename)[0]
            img_path = os.path.join(folder_path, filename)
            image = pygame.image.load(img_path).convert_alpha()
            image = pygame.transform.smoothscale(image, size)
            piece_images[key] = image
    return piece_images

def load_font(font_path, size):
    return pygame.font.Font(font_path, size)
