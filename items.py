import pygame
import math
class Item(pygame.sprite.Sprite):
    def __init__(self, name, stack_max, regen,pos_x,pos_y,type):
        super().__init__()
        self.name = name
        self.image = pygame.image.load(f"Items/{name}.png")
        self.icon = pygame.image.load(f"Items/{name}_icon.png")
        self.font = pygame.font.Font(None, 20)  # Police par défaut, taille 20
        self.stack_max = stack_max
        self.regen = regen
        self.stack = 0
        self.type  = type
        
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

        self.rect_icon = self.icon.get_rect()

        # Variables pour le flottement
        self.base_y = pos_y  # Position de base
        self.flottement_amplitude = 5  # Hauteur du flottement
        self.flottement_vitesse = 0.1  # Vitesse du flottement
        self.time = 0  # Compteur de temps
    
    def update(self,dt):
        self.time += 1
        self.rect.y = self.base_y + int(self.flottement_amplitude * math.sin(self.time * self.flottement_vitesse))
        