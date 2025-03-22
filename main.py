import pygame,sys

from player import *
mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Test")


#Définition de la fenêtre 
screen = pygame.display.set_mode((500,500),pygame.RESIZABLE)

#Instantiation du player
player = Player(0,0,screen)

#Fonction quit
def quit():
    if event.type == QUIT:
            pygame.quit()
            sys.exit()

#Fonction input pour gerer les entrée clavier
def input():
     
     pressed = pygame.key.get_pressed()

     if pressed[pygame.K_UP] or pressed[pygame.K_z]:
          player.move_up()
          

     if pressed[pygame.K_DOWN] or pressed[pygame.K_s] :
          player.move_down()

     if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
          player.move_right()

     if pressed[pygame.K_LEFT] or pressed[pygame.K_q]:
          player.move_left()
    

          

while True : 
    screen.fill((0,0,50))
    
    for event in pygame.event.get():
        quit()
    
    player.affiche()
    input()
    pygame.display.update()
    mainClock.tick(60)