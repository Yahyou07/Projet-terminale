
import pygame

class Player: 
    def __init__(self,pos_x,pos_y,screen):
        self.x = pos_x
        self.y = pos_y
        self.speed = 5
        self.screen = screen

    def affiche(self):
        pygame.draw.rect(self.screen,(125,125,125),(self.x,self.y,50,50))

    def move_right(self):
        self.x +=self.speed
    
    def move_left(self):
        self.x -=self.speed
    
    def move_up(self):
        self.y -=self.speed

    def move_down(self):
        self.y +=self.speed
        