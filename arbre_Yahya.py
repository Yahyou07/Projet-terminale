import pygame
import math

class Arbre(pygame.sprite.Sprite):
    def __init__(self, name, pos_x, pos_y):
        super().__init__()

        self.name = name
        self.image = pygame.image.load(f"Objects/{name}.png")

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    
