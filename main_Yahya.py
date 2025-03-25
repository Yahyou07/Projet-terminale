import pygame,sys
import pytmx
from pytmx.util_pygame import load_pygame
from player_Yahya import *
mainClock = pygame.time.Clock()
from pygame.locals import *
import pyscroll
import pyscroll.data
import time
pygame.init()
pygame.display.set_caption("Test")


#Définition de la fenêtre 
screen = pygame.display.set_mode((1280,720),pygame.RESIZABLE)

# Chargement de la carte Tiled
tmx_data = load_pygame("maps/maps.tmx")  # Remplace par ton fichier .tmx


# Récupérer la position du joueur depuis les objets Tiled
def get_player_spawn():
    for obj in tmx_data.objects:
        if obj.name == "Player":  # L'objet doit s'appeler "Player" dans Tiled
            return obj.x, obj.y
    return 0, 0  # Valeur par défaut si pas trouvé

player_x, player_y = get_player_spawn()
player = Player(player_x, player_y, screen)  # Positionner le joueur
print(player_x,player_y)
# Créer un groupe de rendu pour pyscroll
map_layer = pyscroll.orthographic.BufferedRenderer(pyscroll.data.TiledMapData(tmx_data), screen.get_size())
map_layer.zoom = 2  # Facteur de zoom (1 = taille normale, 2 = zoomé x2)

# Créer un groupe de sprites avec caméra centrée
group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
group.add(player)  # Ajoute le joueur au groupe

#Fonction quit
def quit():
    if event.type == QUIT:
            pygame.quit()
            sys.exit()


#Fonction input pour gerer les entrée clavier
def input():
     pressed = pygame.key.get_pressed()

     moving = False  # Variable pour suivre si une touche de déplacement est pressée
     sprinting = True

     if player.endurance_value == 0:
          sprinting =False

     if pressed[pygame.K_UP] and pressed[pygame.K_r] and sprinting ==True  or pressed[pygame.K_z] and pressed[pygame.K_r] and sprinting ==True :
          player.run_up()
          moving = True

     elif pressed[pygame.K_UP] or pressed[pygame.K_z]:
          player.move_up()
          moving = True

     if pressed[pygame.K_DOWN] and pressed[pygame.K_r] and sprinting ==True or pressed[pygame.K_s] and pressed[pygame.K_r] and sprinting ==True:
          player.run_down()
          moving = True

     elif pressed[pygame.K_DOWN] or pressed[pygame.K_s] :
          player.move_down()
          moving = True
          
     if pressed[pygame.K_RIGHT] and pressed[pygame.K_r] and sprinting ==True or pressed[pygame.K_d] and pressed[pygame.K_r] and sprinting ==True:
          player.run_right()
          moving = True

     elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
          player.move_right()
          moving = True

     if pressed[pygame.K_LEFT] and pressed[pygame.K_r] and sprinting ==True or pressed[pygame.K_q] and pressed[pygame.K_r] and sprinting ==True:
          player.run_left()
          moving = True

     elif pressed[pygame.K_LEFT] or pressed[pygame.K_q]:
          player.move_left()
          moving = True
     
     
     
     if not moving and player.last_direction == "down":
          player.idle_down()
     elif not moving and player.last_direction == "up":
          player.idle_up()
     elif not moving and player.last_direction == "right":
          player.idle_right()
     elif not moving and player.last_direction == "left":
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
    
    group.update()
    group.center(player.rect.center)  # Centre la caméra sur le joueur
    group.draw(screen)
    player.affiche_ui()
    player.regeneration()
    pygame.display.update()
    mainClock.tick(60)