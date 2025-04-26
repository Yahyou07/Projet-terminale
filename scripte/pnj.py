import pygame
import time

class PNJ(pygame.sprite.Sprite):
    """
        Classe représentant un PNJ (Personnage Non Joueur) dans le jeu.
        Le PNJ est initialisé avec une image, une position et un écran.
        attributs:
            x : position initiale x du PNJ
            y : position initiale y du PNJ
            screen : écran sur lequel le PNJ sera affiché
            image_path : chemin de l'image du PNJ
    """
    def __init__(self, x, y, screen, image_path,player_height = None):
        """
            Initialise le PNJ avec une image, une position et un écran
        """
        super().__init__()
        self.spreadsheet = pygame.image.load(image_path).convert_alpha()
        self.crop_rect = pygame.Rect(0, self.spreadsheet.get_height() // 54 * 6, self.spreadsheet.get_width() // 13, self.spreadsheet.get_height() // 54 )
        self.cropped_image = self.spreadsheet.subsurface(self.crop_rect).copy()
        self.pourcent = self.crop_rect.height / player_height
        self.rect = self.cropped_image.get_rect(topleft=(x, y))
        self.image = pygame.transform.scale(self.cropped_image, (int(self.crop_rect.width * self.pourcent), int(self.crop_rect.height * self.pourcent)))
        self.image_color = self.image.get_at((self.image.get_width()-1,self.image.get_height()-1))  # Example: top-left pixel
        self.speed = 1
        self.screen = screen
        self.font = pygame.font.Font("Items/Minecraft.ttf", 14)
        self.collide = False
        self.sprite_index = 0 

        ## Initialisation des listes de mouvement
        self.list_right = self.right()
        self.list_left = self.left()
        self.list_up = self.up()
        self.list_down = self.down()
        self.list_static_right = self.static_right()
        self.list_static_left = self.static_left()
        self.list_static_down = self.static_down()

    def animation(self, list_mouv):
        """
            Fonction qui gère l'animation du PNJ.
            Elle utilise une boucle infinie pour mettre à jour l'image du PNJ en fonction de la direction.
        """
        self.rect.x +=1
        self.sprite_index += self.speed
        if self.sprite_index >= len(list_mouv):
            self.sprite_index = 0
        self.image = list_mouv[int(self.sprite_index)]
    
    def right(self):
        """
            Fonction qui créer une liste d'images pour le mouvement vers la droite.
        """
        self.list_right = list()

        for i in range(12):
            self.list_right.append(pygame.transform.scale(self.spreadsheet.subsurface(pygame.Rect(self.spreadsheet.get_width() // 13 * i, self.spreadsheet.get_height() // 54 * 7, self.spreadsheet.get_width() // 13, self.spreadsheet.get_height() // 54)).copy(), (int(self.spreadsheet.get_width() // 13 * self.pourcent), int(self.spreadsheet.get_height() // 54 * self.pourcent))))
        return self.list_right
    

    def left(self):
        """
            Fonction qui créer une liste d'images pour le mouvement vers la gauche.
        """
        self.list_left = list()
        for i in range(12):
            self.crop_rect = pygame.Rect(self.spreadsheet.get_width() // 13 * i, self.spreadsheet.get_height() // 54 * 5, self.spreadsheet.get_width() // 13, self.spreadsheet.get_height() // 54 )
            self.cropped_image = self.spreadsheet.subsurface(self.crop_rect).copy()
            self.image = self.cropped_image
            self.image = pygame.transform.scale(self.image, (int(self.crop_rect.width * self.pourcent), int(self.crop_rect.height * self.pourcent)))
            self.list_left.append(self.image)
        return self.list_left

    def up(self):
        """
            Fonction qui créer une liste d'images pour le mouvement vers le haut.
        """
        self.list_up = list()
        for i in range(12):
            self.crop_rect = pygame.Rect(self.spreadsheet.get_width() // 13 * i, self.spreadsheet.get_height() // 54 * 4, self.spreadsheet.get_width() // 13, self.spreadsheet.get_height() // 54 )
            self.cropped_image = self.spreadsheet.subsurface(self.crop_rect).copy()
            self.image = self.cropped_image
            self.image = pygame.transform.scale(self.image, (int(self.crop_rect.width * self.pourcent), int(self.crop_rect.height * self.pourcent)))
            self.list_up.append(self.image)
        return self.list_up

    def down(self):
        """
            Fonction qui créer une liste d'images pour le mouvement vers le bas.
        """
        self.list_down = list()
        for i in range(12):
            self.crop_rect = pygame.Rect(self.spreadsheet.get_width() // 13 * i, self.spreadsheet.get_height() // 54 * 6, self.spreadsheet.get_width() // 13, self.spreadsheet.get_height() // 54 )
            self.cropped_image = self.spreadsheet.subsurface(self.crop_rect).copy()
            self.image = self.cropped_image
            self.image = pygame.transform.scale(self.image, (int(self.crop_rect.width * self.pourcent), int(self.crop_rect.height * self.pourcent)))
            self.list_down.append(self.image)
        return self.list_down

    def static_right(self):
        """
            Fonction qui créer une liste d'images pour le mouvement statique vers la droite.
        """
        self.list_static_right = list()
        for i in range(6):
            self.crop_rect = pygame.Rect(self.spreadsheet.get_width() // 13 * i, self.spreadsheet.get_height() // 54 * 3, self.spreadsheet.get_width() // 13, self.spreadsheet.get_height() // 54 )
            self.cropped_image = self.spreadsheet.subsurface(self.crop_rect).copy()
            self.image = self.cropped_image
            self.image = pygame.transform.scale(self.image, (int(self.crop_rect.width * self.pourcent), int(self.crop_rect.height * self.pourcent)))
            self.list_static_right.append(self.image)
        return self.list_static_right

    def static_left(self):
        """
            Fonction qui créer une liste d'images pour le mouvement statique vers la gauche.
        """
        self.list_static_left = list()
        for i in range(6):
            self.crop_rect = pygame.Rect(self.spreadsheet.get_width() // 13 * i, self.spreadsheet.get_height() // 54 * 1, self.spreadsheet.get_width() // 13, self.spreadsheet.get_height() // 54 )
            self.cropped_image = self.spreadsheet.subsurface(self.crop_rect).copy()
            self.image = self.cropped_image
            self.image = pygame.transform.scale(self.image, (int(self.crop_rect.width * self.pourcent), int(self.crop_rect.height * self.pourcent)))
            self.list_static_left.append(self.image)
        return self.list_static_left

    def static_down(self):
        """
            Fonction qui créer une liste d'images pour le mouvement statique vers le bas.
        """
        self.list_static_down = list()
        for i in range(6):
            self.crop_rect = pygame.Rect(self.spreadsheet.get_width() // 13 * i, self.spreadsheet.get_height() // 54 * 2, self.spreadsheet.get_width() // 13, self.spreadsheet.get_height() // 54 )
            self.cropped_image = self.spreadsheet.subsurface(self.crop_rect).copy()
            self.image = self.cropped_image
            self.image = pygame.transform.scale(self.image, (int(self.crop_rect.width * self.pourcent), int(self.crop_rect.height * self.pourcent)))
            self.list_static_down.append(self.image)
        return self.list_static_down


    def static(self):
        """
            Fonction qui affiche le PNJ sans le déplacer.
        """
        self.static = True
        self.crop_rect = pygame.Rect(0, self.image.get_height() // 54 * 6, self.image.get_width() // 13, self.image.get_height() // 54 )
        while self.static:
            time.sleep(0.01)  # Pause de 0.01 seconde pour ralentir le mouvement
            if self.crop_rect.x < self.spreadsheet.get_width() // 13 :
                self.crop_rect.x += self.spreadsheet.get_width() // 13
            elif self.crop_rect.x == self.spreadsheet.get_width() // 13 :
                self.crop_rect.x = 0
            self.cropped_image = self.spreadsheet.subsurface(self.crop_rect).copy()
            self.image = self.cropped_image
            self.image = pygame.transform.scale(self.image, (int(self.crop_rect.width * self.pourcent), int(self.crop_rect.height * self.pourcent)))
            self.screen.blit(self.image, self.rect) # on affiche le PNJ à sa nouvelle position
            pygame.display.flip()   # on met à jour l'affichage

    def haut(self):
        """
            Fonction qui déplace le PNJ vers le haut.
        """
        self.top = True
        self.crop_rect = pygame.Rect(0, self.image.get_height() // 54 * 4, self.image.get_width() // 13, self.image.get_height() // 54 )
        self.cropped_image = self.spreadsheet.subsurface(self.crop_rect).copy()
        self.image = self.cropped_image
        self.image = pygame.transform.scale(self.image, (int(self.crop_rect.width * self.pourcent), int(self.crop_rect.height * self.pourcent)))
        while self.top:
            time.sleep(0.01)  # Pause de 0.01 seconde pour ralentir le mouvement
            self.rect.y -= 1
            if self.crop_rect.x < self.spreadsheet.get_width() // 13 :
                self.crop_rect.x += self.spreadsheet.get_width() // 13
            elif self.crop_rect.x == self.spreadsheet.get_width() // 13 :
                self.crop_rect.x = 0
            self.cropped_image = self.spreadsheet.subsurface(self.crop_rect).copy()
            self.image = self.cropped_image
            self.image = pygame.transform.scale(self.image, (int(self.crop_rect.width * self.pourcent), int(self.crop_rect.height * self.pourcent)))
            self.screen.blit(self.image, self.rect)
            pygame.display.update() 
        
        
    
    def bas(self):
        """
            Fonction qui déplace le PNJ vers le bas.
        """
        self.bottom = True
        self.crop_rect = pygame.Rect(0, self.image.get_height() // 54 * 6, self.image.get_width() // 13, self.image.get_height() // 54 )
        self.cropped_image = self.spreadsheet.subsurface(self.crop_rect).copy()
        self.image = self.cropped_image
        self.image = pygame.transform.scale(self.image, (int(self.crop_rect.width * self.pourcent), int(self.crop_rect.height * self.pourcent)))
        while self.bottom:
            self.screen.fill((0, 0, 0))  # Efface l'écran
            self.image.fill((0, 0, 0))  # Efface l'image
            time.sleep(0.01)  # Pause de 0.01 seconde pour ralentir le mouvement
            self.rect.y += 1
            if self.crop_rect.x < self.spreadsheet.get_width() // 13 :
                self.crop_rect.x += self.spreadsheet.get_width() // 13
            elif self.crop_rect.x == self.spreadsheet.get_width() // 13 :
                self.crop_rect.x = 0
            self.cropped_image = self.spreadsheet.subsurface(self.crop_rect).copy()
            self.image = self.cropped_image
            self.image = pygame.transform.scale(self.image, (int(self.crop_rect.width * self.pourcent), int(self.crop_rect.height * self.pourcent)))
            self.screen.blit(self.image, self.rect)
            pygame.display.update()   
    
    def gauche(self):
        """
            Fonction qui déplace le PNJ vers la gauche.
        """
        self.left = True
        self.crop_rect = pygame.Rect(0, self.image.get_height() // 54 * 5, self.image.get_width() // 13, self.image.get_height() // 54 )
        self.cropped_image = self.spreadsheet.subsurface(self.crop_rect).copy()
        self.image = self.cropped_image
        self.image = pygame.transform.scale(self.image, (int(self.crop_rect.width * self.pourcent), int(self.crop_rect.height * self.pourcent)))
        while self.left:
            time.sleep(0.01)
            self.rect.x -= 1
            if self.crop_rect.x < self.spreadsheet.get_width() // 13 :
                self.crop_rect.x += self.spreadsheet.get_width() // 13
            elif self.crop_rect.x == self.spreadsheet.get_width() // 13 :
                self.crop_rect.x = 0
            self.cropped_image = self.spreadsheet.subsurface(self.crop_rect).copy()
            self.image = self.cropped_image
            self.image = pygame.transform.scale(self.image, (int(self.crop_rect.width * self.pourcent), int(self.crop_rect.height * self.pourcent)))
            self.screen.blit(self.image, self.rect)
            pygame.display.update()

    def droite(self):
        """
            Fonction qui déplace le PNJ vers la droite.
        """
        self.right = True
        self.crop_rect = pygame.Rect(0, self.spreadsheet.get_height() // 54 * 7, self.spreadsheet.get_width() // 13, self.spreadsheet.get_height() // 54 )
        self.cropped_image = self.spreadsheet.subsurface(self.crop_rect).copy()
        self.image = self.cropped_image
        self.image = pygame.transform.scale(self.image, (int(self.crop_rect.width * self.pourcent), int(self.crop_rect.height * self.pourcent)))
        self.rect.x += 1
        if self.crop_rect.x < self.spreadsheet.get_width() // 13 :
                self.crop_rect.x += self.spreadsheet.get_width() // 13
        elif self.crop_rect.x == self.spreadsheet.get_width() // 13 :
                self.crop_rect.x = 0
        self.cropped_image = self.spreadsheet.subsurface(self.crop_rect).copy()
        self.image = self.cropped_image
        self.image = pygame.transform.scale(self.image, (int(self.crop_rect.width * self.pourcent), int(self.crop_rect.height * self.pourcent)))
        self.screen.blit(self.image, self.rect)
            
    def pattern(self,lim_x1,lim_y1,lim_x2,lim_y2):
        """
            Fonction génératrice qui gère le mouvement du PNJ dans un motif spécifique.
            Le PNJ se déplace entre les limites spécifiées (lim_x1, lim_y1) et (lim_x2, lim_y2).
            attributs:
                lim_x1 : limite x1 pour la position du PNJ
                lim_y1 : limite y1 pour la position du PNJ
                lim_x2 : limite x2 pour la position du PNJ
                lim_y2 : limite y2 pour la position du PNJ
            yield : renvoie la position actuelle du PNJ
        """
        assert lim_x1 < lim_x2, "lim_x1 doit être inférieur à lim_x2"
        assert lim_y1 < lim_y2, "lim_y1 doit être inférieur à lim_y2"
        assert self.rect.x >= lim_x1 and self.rect.x <= lim_x2, "La position x du PNJ doit être comprise entre lim_x1 et lim_x2"
        assert self.rect.y >= lim_y1 and self.rect.y <= lim_y2, "La position y du PNJ doit être comprise entre lim_y1 et lim_y2"
        assert self.rect.x == lim_x1 or self.rect.x == lim_x2, "La position x du PNJ doit être égale à lim_x1 ou lim_x2"
        assert self.rect.y == lim_y1 or self.rect.y == lim_y2, "La position y du PNJ doit être égale à lim_y1 ou lim_y2"
        assert self.rect.x == lim_x1 and self.rect.y == lim_y1 or self.rect.x == lim_x2 and self.rect.y == lim_y2, "La position du PNJ doit être égale à (lim_x1, lim_y1) ou (lim_x2, lim_y2)"
        assert self.rect.x != lim_x1 or self.rect.y != lim_y1 or self.rect.x != lim_x2 or self.rect.y != lim_y2, "La position du PNJ ne doit pas être égale à (lim_x1, lim_y1) ou (lim_x2, lim_y2) en même temps"

        while not self.collide: # on lui fait faire suivre un patern tant qu'il n'y a pas de collision
            time.sleep(0.01)  # Pause de 0.01 seconde pour ralentir le mouvement
            if self.rect.x >= lim_x1 and self.rect.y == lim_y1:
                self.animation(self.list_right) # on lui fait faire une animation de marche vers la droite
            elif self.rect.x == lim_x2 and self.rect.y == lim_y1:
                self.right = False
                self.top = False
                self.left = False
                self.bas()
            elif self.rect.x == lim_x2 and self.rect.y == lim_y2:
                self.bottom = False
                self.right = False
                self.top = False
                self.gauche()
            elif self.rect.x == lim_x1 and self.rect.y == lim_y2:
                self.left = False
                self.bottom = False
                self.right = False
                self.haut()

    
    
    
        

        
    
        