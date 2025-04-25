import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self,name,x,y,type,screen):
        super().__init__()
        self.name = name
        self.image = pygame.image.load(f"{type}/{name}/idle/idle1.png")
        self.right_move = [pygame.image.load(f"{type}/{name}/walk/walk1/right{i}.png")for i in range(1,10)]
        self.idle_move = [pygame.image.load(f"{type}/{name}/idle/idle{i}.png")for i in range(1,4)]
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y
        self.hit_box = self.rect.copy().inflate(-30,0)
        self.champ_vision = self.rect.copy().inflate(20,20)

        self.sprite_index = 0
        self.parole = None
        self.right = True
        self.dialog_box = pygame.image.load("UI/dialog_box_gris.png")
        self.dialog_box_name = pygame.image.load("UI/dialog_box_nom.png")
        self.portrait = pygame.image.load(f"{type}\{name}\portrait2.png")
        self.screen = screen

        self.CanDialog = False
    def animation(self,list_mouv,speed):
        self.sprite_index += speed
        if self.sprite_index >=len(list_mouv):
            self.sprite_index = 0
        self.image = list_mouv[int(self.sprite_index)]
        self.image = pygame.transform.scale(self.image,(50,50))

    def droite(self):
        self.rect.x += 1
        self.animation(self.right_move,0.20)
        
    def idle(self):
        self.animation(self.idle_move,0.12)

    def haut(self):
        self.rect.y += 1

    def bas(self):
        self.rect.y -= 1

    def gauche(self):
        self.rect.x -= 1

    def update(self):
        if self.CanDialog:
            self.screen.blit(self.dialog_box,(300,600))
            self.screen.blit(self.portrait,(360,500))
            self.screen.blit(self.dialog_box_name,(350,750))
        
        

# On crée ici une classe qui hérite de la classe Entity
class PNJ(Entity):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        pass
