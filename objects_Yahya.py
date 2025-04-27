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

class Coffre(pygame.sprite.Sprite):
    def __init__(self, name, x,y):
        super().__init__()
        self.name = name

        self.coffre_open_list = [pygame.image.load(f"Objects/{name}/frame{j}.png") for j in range(0, 12)]
        self.current_chest = 0
        self.image = pygame.image.load(f"Objects/{name}/frame0.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.Can_open = True

        # Parramètre à utiliser pour l'animation 
        self.coffre_anim = False
        self.coffre_animation_list = []
        self.coffre_anim_speed = 0
        self.coffre_anim_index = 0
        

    def start_animation_coffre(self,list_mouv,speed):
        self.coffre_animation_list = list_mouv
        self.coffre_anim_speed = speed
        self.coffre_anim_index = 0
        self.coffre_anim = True

    def anim_chest(self):
        if self.coffre_anim:
            self.coffre_anim_index += self.coffre_anim_speed
           
            # Si l'index est supérieur a la taille de la liste de mouvement :
            if self.coffre_anim_index >= len(self.coffre_animation_list):
                
                self.coffre_anim = False # Alors on arrete le processus en mettant le booleen a False
                self.coffre_anim_index = len(self.coffre_animation_list) - 1  #Et on desincrémente l'index pour ne pas être out of range
                self.Can_open = False
            # Si l'index est négatif     
            elif self.coffre_anim_index < 0: 
                self.coffre_anim_index = 0  # Alors on le remet a zero
            self.image = self.coffre_animation_list[int(self.coffre_anim_index)] # On change l'image de base par l'image de la liste de mouvment du current_index

class Crater(pygame.sprite.Sprite):
    def __init__(self,name,x,y):
        super().__init__()
        self.name = name
        self.image = pygame.image.load(f"enemy/{name}.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        