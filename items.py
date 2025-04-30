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

        # Animation de sortie de coffre
        self.en_animation_sortie = False
        self.vitesse_x = 0
        self.vitesse_y = 0
        self.gravite = 0.5  # Accélération due à la gravité

    def lancer_depuis_coffre(self, direction='droite'):
        self.en_animation_sortie = True
        force = 5
        self.vitesse_y = -force  # vers le haut

        if direction == 'droite':
            self.vitesse_x = 2
        else:
            self.vitesse_x = -2

    def update(self, dt):
        if self.en_animation_sortie:
            self.vitesse_y += self.gravite
            self.rect.x += int(self.vitesse_x)
            self.rect.y += int(self.vitesse_y)

            # Stopper l’animation quand l’objet touche le sol
            if self.rect.y >= self.base_y:
                self.rect.y = self.base_y
                self.en_animation_sortie = False
                self.vitesse_x = 0
                self.vitesse_y = 0
        else:
            # Flottement classique
            self.time += 1
            self.rect.y = self.base_y + int(self.flottement_amplitude * math.sin(self.time * self.flottement_vitesse))

        