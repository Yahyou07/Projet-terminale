import pygame,sys
import pytmx
from pytmx.util_pygame import load_pygame
import pytmx.util_pygame
from player_Yahya import *
from items import *
mainClock = pygame.time.Clock()
from pygame.locals import *
import pyscroll
import pyscroll.data
import time
pygame.init()
pygame.display.set_caption("Jeu")


#Définition de la fenêtre 
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Chargement de la carte Tiled
tmx_data = load_pygame("maps/maps.tmx")  # Remplace par ton fichier .tmx


# Récupérer la position du joueur depuis les objets Tiled


player_position = tmx_data.get_object_by_name("Player")
player = Player(player_position.x,player_position.y, screen)  # Positionner le joueur

item = Item(352,353,screen)

map_data = pyscroll.data.TiledMapData(tmx_data)

# Créer un groupe de rendu pour pyscroll
map_layer = pyscroll.orthographic.BufferedRenderer(map_data, screen.get_size())
map_layer.zoom = 2  # Facteur de zoom (1 = taille normale, 2 = zoomé x2)

# Créer un groupe de sprites avec caméra centrée
group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

group.add(player)  # Ajoute le joueur au groupe
group.add(item)
#Fonction quit
def quit():
    if event.type == QUIT:
            pygame.quit()
            sys.exit()
    elif event.type == pygame.KEYDOWN:  # Si une touche est pressée
            if event.key == pygame.K_ESCAPE:  # Si la touche pressée est "Échap"
                pygame.quit()
                sys.exit()
    


#Fonction input pour gerer les entrée clavier
def input():
    pressed = pygame.key.get_pressed()
    dx, dy = 0, 0
    sprinting = pressed[pygame.K_r] and player.endurance_value > 0 and player.Regen ==False  # Vérifie si le joueur peut sprinter

    if pressed[pygame.K_UP] or pressed[pygame.K_z]:
        dy = -1
    if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
        dy = 1
    if pressed[pygame.K_LEFT] or pressed[pygame.K_q]:
        dx = -1
    if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
        dx = 1
    
    if dx != 0 or dy != 0:
        player.move(dx, dy, sprinting)  # Passe la variable sprinting
    else:
        # Animation idle quand le joueur ne bouge pas
        if player.last_direction == "down":
            player.idle_down()
        elif player.last_direction == "up":
            player.idle_up()
        elif player.last_direction == "right":
            player.idle_right()
        elif player.last_direction == "left":
            player.idle_left()

     

def handle_resize(event):
    if event.type == pygame.VIDEORESIZE:
        new_size = (event.w, event.h)  # Nouvelle taille de la fenêtre
        pygame.display.set_mode(new_size, pygame.RESIZABLE)  # Appliquer le resize
    

while True : 

    for event in pygame.event.get():
        quit()
        handle_resize(event)  # Gérer le redimensionnement
        
                
        
    input()

    keys = pygame.key.get_pressed()
    player.regeneration_endurance(keys)
    item.update()
    group.update()
    group.center(player.rect.center)  # Centre la caméra sur le joueur
    group.draw(screen)
    player.affiche_ui()
    
    pygame.display.update()
    mainClock.tick(60)