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




player_position = tmx_data.get_object_by_name("Player")
player = Player(player_position.x,player_position.y, screen)  # Positionner le joueur

item = Item("pain",24,10,352,350,"Food")
item2 = Item("plastron",1,10,300,450,"Plastron")
item3 = Item("apple",24,10,352,290,"Food")
item4 = Item("bottes",1,10,500,270,"Bottes")
item5 = Item("fromage",24,10,330,500,"Food")
item6 = Item("rubis",24,10,352,530,"Food")
item7 = Item("casque",1,10,180,560,"Casque")
item8 = Item("jambiere",1,10,352,230,"Jambiere")
item9 = Item("pain",24,10,352,700,"Food")
item10 = Item("fish",24,10,352,710,"Food")
item11 = Item("fromage",24,10,352,130,"Food")
item12 = Item("fromage",24,10,400,130,"Food")



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

curent_quantity = 0

#parametres la progression du cercle pour le "manger"
fill_time = 3.0 # Durée du remplissage
progress = 0.0
progressing = False
finished_time = 0
show_message = False


#Booléens : 
show_inventory = False #booléen pour gérer l'affichage de l'inventaire
moving = True #booléen pour gérer le droit de mouvment du personnage

while True : 
    dt = mainClock.tick(60) / 1000  # Temps écoulé en secondes

    for event in pygame.event.get():
        quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                show_inventory = not show_inventory  # On inverse l'état de l'inventaire
                player.OnBag = True
                player.OnArmour = False
                moving = not moving
        #Lorsqu'on clique sur l'icone de l'armure on passe sur l'armure du joueur
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if player.rect_button_armour.collidepoint(event.pos) :
                    player.OnArmour = True
                    player.OnBag = False
        #Lorsqu'on clique sur l'icone du sac on passe sur l'inventaire
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if player.rect_button_bag.collidepoint(event.pos) :
                    
                    player.OnArmour = False
                    player.OnBag = True
        
            

        if show_inventory:
            
                player.handle_mouse_events(event)
        player.handle_key_events(event)

    #verifier si l'on peut marcher
    if moving:
        input()
    
    # Clic droit maintenu pour gréer l'affichage du "progress circle"
    if player.inventory_bar_list[player.inventory_index] != {}:
        if player.inventory_bar_list[player.inventory_index]['object'].type == "Food" : 
            if player.health_value < 100:
                if pygame.mouse.get_pressed()[2]:
                    if not progressing:
                        progressing = True
                        progress = 0.0
                    else:
                        progress += dt / fill_time
                        if progress >= 1.0:
                            progressing = False
                            show_message = True
                            print("Nourriture consommé")
                            player.eat(player.inventory_index) #On active la méthode eat lorsque "la progress circle" se termine
                            finished_time = pygame.time.get_ticks()
                else:
                    if progress < 1.0:
                        progressing = False
                        progress = 0.0
    


    

    
    keys = pygame.key.get_pressed()
    player.regeneration_endurance(keys)
    
    group.update()
    group.center(player.rect.center)  # Centre la caméra sur le joueur
    group.draw(screen)
    player.affiche_ui()
    


    if progressing:
        world_pos = (player.rect.centerx + 25, player.rect.top - 10)
        screen_pos = map_layer.translate_point(world_pos)

        radius = 30
        end_angle = -math.pi / 2 + progress * 2 * math.pi
        pygame.draw.circle(screen, (100, 100, 100), screen_pos, radius, 3)
        pygame.draw.arc(screen, (0, 200, 0),
                        (screen_pos[0] - radius, screen_pos[1] - radius, radius * 2, radius * 2),
                        -math.pi / 2, end_angle, 4)

    
         

    for sprite in group.sprites():
        if isinstance(sprite, Item) and player.rect.colliderect(sprite.rect):
            #print("Collision detectee avec",sprite.name)
            group.remove(sprite)  # Supprime l'objet du groupe
            player.add_to_inventory(sprite)
            
            '''
            print("**barre d'inventaire**")
            print(player.inventory_bar_list)
            print()
            print("**Inventaire**")
            for i in player.inventory_list:
                print(i)
            print("")
            print("**Armour list**")
            '''
            
            

    if show_inventory:
            player.display_inventory()  # On appelle la méthode display_inventory pour afficher l'inventaire 
        
    

    pygame.display.update()
    
   