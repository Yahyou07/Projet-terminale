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

item = Item("apple",1,10,352,350)
item2 = Item("plastron",1,10,352,450)
item3 = Item("apple",1,10,352,290)
item4 = Item("apple",1,10,352,270)
item5 = Item("hache",1,10,352,500)
item6 = Item("apple",1,10,352,530)
item7 = Item("apple",1,10,352,560)
item8 = Item("hache",1,10,352,230)
item9 = Item("pioche",1,10,352,700)
item10 = Item("hache",1,10,352,350)
item11 = Item("pain",1,10,360,200)

item12 = Item("apple",1,10,352,560)
item13 = Item("hache",1,10,352,230)
item14 = Item("pioche",1,10,352,700)
item15 = Item("hache",1,10,352,350)
item16 = Item("pain",1,10,360,200)

item17 = Item("apple",1,10,352,180)
item18 = Item("pain",1,10,360,150)

map_data = pyscroll.data.TiledMapData(tmx_data)

# Créer un groupe de rendu pour pyscroll
map_layer = pyscroll.orthographic.BufferedRenderer(map_data, screen.get_size())
map_layer.zoom = 2  # Facteur de zoom (1 = taille normale, 2 = zoomé x2)

# Créer un groupe de sprites avec caméra centrée
group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

# Ajoute les objets au groupe
group.add(player)  
group.add(item)
group.add(item2)
group.add(item3)
group.add(item4)
group.add(item5)
group.add(item6)
group.add(item7)
group.add(item8)
group.add(item9)
group.add(item10)
group.add(item11)

group.add(item12)
group.add(item13)
group.add(item14)
group.add(item15)
group.add(item16)
group.add(item17)
group.add(item18)

if player.rect.colliderect(item.rect):
    print("Collision détectée !")
    item.kill()  # Supprime l’item
else:
    print("Aucune collision détectée")

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
    attacking = 0
    sprinting = pressed[pygame.K_r] and player.endurance_value > 0 and player.Regen ==False  # Vérifie si le joueur peut sprinter

    if pressed[pygame.K_UP] or pressed[pygame.K_z]:
        dy = -1
    if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
        dy = 1
    if pressed[pygame.K_LEFT] or pressed[pygame.K_q]:
        dx = -1
    if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
        dx = 1
    
    # si le bouton est pressé, le perso attaque
    if pressed[pygame.K_a]:
        attacking = 1
        dx = 0
        dy = 0

    if dx != 0 or dy != 0:
        player.move(dx, dy, attacking, sprinting)  # Passe la variable sprinting

    if attacking == 1:
        player.move(dx, dy, attacking, sprinting)

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

curent_quantity = 0

show_inventory = False
while True : 

    for event in pygame.event.get():
        quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                show_inventory = not show_inventory  # On inverse l'état de l'inventaire
        if show_inventory:
            player.drag_and_drop_inventory(event)

    input()

    keys = pygame.key.get_pressed()
    player.regeneration_endurance(keys)
    
    group.update()
    group.center(player.rect.center)  # Centre la caméra sur le joueur
    group.draw(screen)
    player.affiche_ui()
    

    for sprite in group.sprites():
        if isinstance(sprite, Item) and player.rect.colliderect(sprite.rect):
            print("Collision detectee avec",sprite.name)
            group.remove(sprite)  # Supprime l'objet du groupe
            player.add_to_inventory(sprite)
            
            print("**barre d'inventaire**")
            print(player.inventory_bar_list)
            print()
            print("**Inventaire**")
            
            for i in player.inventory_list:
                print(i)

    if show_inventory:
        player.display_inventory()  # Appelle une méthode pour afficher l'inventaire 

    pygame.display.update()
    mainClock.tick(60)
   