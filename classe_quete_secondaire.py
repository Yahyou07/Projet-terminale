import pygame
import sys

class Quetes_secondaire(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.recompense = None
        self.dialogue = None
        self.mission = None


    def lancer_quete(self):
        pass

    def arreter_quete(self):
        pass
    
    