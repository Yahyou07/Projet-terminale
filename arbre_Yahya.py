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


        self.liste_image_fumee = []
        self.image_fumee = None
        self.Can_cut = True

        
class Tronc(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Objects/tronc1.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.Can_cut = True
        self.hitbox = self.rect.copy().inflate(-63, -106)
        self.hitbox.y +=43
        self.hitbox.x +=2

class Feuillage(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Objects/feuillage1.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
