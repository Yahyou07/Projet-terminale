
import pygame

class Quete_Principale(pygame.sprite.Sprite):
    def __init__(self,name):
        super().__init__()
        self.name = name
        self.mission = None
        self.recompense = None
        self.map = None
        self.entite = None
        self.dialogue = None
        self.avancement = 0

    def lancer_quêtes(self):
        pass

    def arreter_quetes(self):
        pass
    def afficher_quete(self):
        pass




        