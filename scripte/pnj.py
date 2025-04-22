import pygame

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
    def __init__(self, x, y, screen, image_path):
        """
            Initialise le PNJ avec une image, une position et un écran
        """
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.crop_rect = pygame.Rect(0, self.image.get_height() // 54 * 2, self.image.get_width() // 13, self.image.get_height() // 54 )
        self.cropped_image = self.image.subsurface(self.crop_rect).copy()
        self.image = self.cropped_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.screen = screen
        self.font = pygame.font.Font("Items/Minecraft.ttf", 14)
        self.collide = False
    
    def static(self):
        """
            Fonction qui affiche le PNJ sans le déplacer.
        """
        self.crop_rect = pygame.Rect(self.image.x, self.image.y, self.image.get_width()//13, self.image.get_height()//54 * 3)
        self.cropped_image = pygame.Surface((self.crop_rect.width, self.crop_rect.height), pygame.SRCALPHA)
        self.image = self.cropped_image
        self.screen.blit(self.image, self.rect)
        pygame.display.flip()

    def haut(self):
        """
            Fonction qui déplace le PNJ vers le haut.
        """
        self.rect.y -= 1
        self.screen.blit(self.image, self.rect)
        pygame.display.flip()
    
    def bas(self):
        """
            Fonction qui déplace le PNJ vers le bas.
        """
        self.rect.y += 1
        self.screen.blit(self.image, self.rect)
        pygame.display.flip()
    
    def gauche(self):
        """
            Fonction qui déplace le PNJ vers la gauche.
        """
        self.rect.x -= 1
        self.screen.blit(self.image, self.rect)
        pygame.display.flip()

    def droite(self):
        """
            Fonction qui déplace le PNJ vers la droite.
        """
        self.rect.x += 1
        self.screen.blit(self.image, self.rect)
        pygame.display.flip()

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

        while not self.collide: # on lui fait faire suivre un patern
            if self.rect.x >= lim_x1 and self.rect.x < lim_x2:
                self.droite()
            elif self.rect.x == lim_x2 and self.rect.x > lim_x1:
                continue
            elif self.rect.y >= lim_y1 and self.rect.y < lim_y2:
                self.bas()
            elif self.rect.y == lim_y2 and self.rect.y > lim_y1:
                continue
            elif self.rect.x == lim_x2 and self.rect.y == lim_y2:
                self.gauche()
            elif self.rect.x == lim_x1 and self.rect.y == lim_y2:
                self.haut()
            elif self.rect.x == lim_x1 and self.rect.y == lim_y1:
                self.droite()
            yield self.rect.x, self.rect.y
            self.screen.blit(self.image, self.rect)
            pygame.display.flip()
    
    
    
        

        
    
        