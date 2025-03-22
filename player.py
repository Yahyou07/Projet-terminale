
import pygame

class Player: 
    def __init__(self,pos_x,pos_y,screen):
        self.x = pos_x
        self.y = pos_y
        self.speed = 3
        self.screen = screen
        self.image = pygame.image.load("anim\idle1.png")


        self.images = [pygame.image.load("anim\idle1.png"),
                       pygame.image.load("anim\idle2.png"),
                       pygame.image.load("anim\idle3.png"),
                       pygame.image.load("anim\idle4.png")]
        self.rectangle = self.image.get_rect()

    def affiche(self):
        self.screen.blit(self.image,(self.x,self.y))


    
    def move_left(self):
        self.x -=self.speed
        self.image = self.images[3]
    
    def move_right(self):
        self.x +=self.speed
        self.image = self.images[2]
    
    def move_up(self):
        self.y -=self.speed
        self.image = self.images[1]

    def move_down(self):
        self.y +=self.speed
        self.image = self.images[0]
        