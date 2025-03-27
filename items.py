import pygame
import math
class Item(pygame.sprite.Sprite): 
    def __init__(self,pos_x,pos_y,screen):
        super().__init__()  # Initialisation du sprite

        self.screen = screen
        self.image= pygame.image.load("Items/pomme.png")
        #self.image = pygame.transform.scale(self.image, (32,32 ))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
    

        # Variables pour le flottement
        self.base_y = pos_y  # Position de base
        self.flottement_amplitude = 5  # Hauteur du flottement
        self.flottement_vitesse = 0.05  # Vitesse du flottement
        self.time = 0  # Compteur de temps

    def update(self):
        
        self.time += 1
        self.rect.y = self.base_y + int(self.flottement_amplitude * math.sin(self.time * self.flottement_vitesse))