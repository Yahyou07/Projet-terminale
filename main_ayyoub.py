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
from scripte.enigme import*
from scripte.save_game import*
pygame.init()
pygame.display.set_caption("Jeu")

dico = """{
    'question 1 : Qui est le singe' : ['réponse A : Tu es fous','réponse B : Tu es fouuu','réponse C : Tu es picece','réponse D : rhgreg','bonne réponse : Tu es fous'],
    'question 2 : Quelle est la couleur du ciel ?' : ['réponse A : Rouge','réponse B : Bleu','réponse C : Vert','réponse D : Noir','bonne réponse : Bleu']
}"""

#Définition de la fenêtre 
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


# Chargement de la carte Tiled
tmx_data = load_pygame("maps/maps.tmx")  # Remplace par ton fichier .tmx

dicco = Enigme(dico,screen)
save_menu = Save_game(screen)
# Récupérer la position du joueur depuis les objets Tiled


player_position = tmx_data.get_object_by_name("Player")
player = Player(player_position.x,player_position.y, screen)  # Positionner le joueur

item = Item("pain",24,10,352,350,"Food")
item2 = Item("plastron",1,10,352,450,"Plastron")
item3 = Item("apple",24,10,352,290,"Food")
item4 = Item("bottes",24,10,352,270,"Bottes")
item5 = Item("fromage",1,10,352,500,"Food")
item6 = Item("rubis",24,10,352,530,"Food")
item7 = Item("casque",24,10,352,560,"Casque")
item8 = Item("jambiere",1,10,352,230,"Jambiere")
item9 = Item("pain",1,10,352,700,"Food")
item10 = Item("fish",24,10,352,710,"Food")
item11 = Item("fromage",24,10,352,130,"Food")
item12 = Item("fromage",1,10,352,130,"Food")



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

curent_quantity = 0

show_inventory = False
while True : 
    for event in pygame.event.get():
        quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                show_inventory = not show_inventory  # On inverse l'état de l'inventaire
        if show_inventory:
            player.handle_mouse_events(event)
        save_menu.handle_event(event,"ruen",1,player.rect.x,player.rect.y)

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
        
    
    save_menu.update()
    pygame.display.update()
    mainClock.tick(60)
   