import pygame,sys

mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Test")

#Fonction quit
def quit():
    if event.type == QUIT:
            pygame.quit()
            sys.exit()

#Définition de la fenêtre 
screen = pygame.display.set_mode((500,500),pygame.RESIZABLE)

while True : 
    screen.fill((0,0,50))

    for event in pygame.event.get():
        quit()

    pygame.display.update()
    mainClock.tick(60)