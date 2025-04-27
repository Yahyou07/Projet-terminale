
import random

def generate_tree_positions(max_x, max_y, num_trees, min_distance, max_attempts=1000):
    positions = []
    for i in range(num_trees):
        attempt = 0
        while attempt < max_attempts:
            pos = (random.randint(0, max_x), random.randint(0, max_y))
            if all(abs(pos[0] - x) > min_distance and abs(pos[1] - y) > min_distance for x, y in positions):
                positions.append(pos)
                break
            attempt += 1
        
    return positions


#tree_positions = [(216, 860), (1430, 1322), (1026, 1471), (20, 537), (899, 706), (1332, 1150), (1124, 395), (698, 252), (816, 18), (1513, 1237), (327, 119), (479, 1026), (613, 619),(114,1460),(298,1460)]
tree_positions = [
                   (931, 1390), (383, 1226), (450, 199), (1030, 190),
                   (9, 341), (83, 49), (1331, 1053), (1522, 1112), 
                   (137, 941), (192, 757), (1182, 897), (1264, 1498), 
                   (297, 705), (550, 705), (585, 1300)
                   ]


import pygame, sys
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
from objects_Yahya import *
from random import *
pygame.init()
pygame.display.set_caption("Jeu")
from scripte.save_game import*
from classe_enemy_Yahya import *
from scripte.pnj import *
import pygame
from classe_entity_Yahya import *
from dialog_data import *

# Définition de la fenêtre
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Chargement de la carte Tiled
tmx_data = load_pygame("maps/maps.tmx")  


collision_rects = []

for obj in tmx_data.objects:
    if obj.name == "collision" or obj.type == "collision":
        rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
        collision_rects.append(rect)


player_position = tmx_data.get_object_by_name("Player")
player = Player(player_position.x, player_position.y, screen)  # Positionner le joueur

save_menu = Save_game(screen)
chest_position = tmx_data.get_object_by_name("coffre1")

pnj1 = PNJ("Wizard",200,200,"pnj",screen,pnj1_dialog)

#Création des gobelins
gobelin1 = Enemy("gobelin_epee",250,300,"enemy",screen)

gobelin2 = Enemy("gobelin_epee",350,250,"enemy",screen)

gobelin3 = Enemy("gobelin_epee",350,400,"enemy",screen)

slime1 = Slime("slime","enemy",600,100)
#pnj2 = PNJ("Wizard",200,500,"pnj",screen)
chest1 = Coffre("chest1",chest_position.x,chest_position.y)

item = Item("pain", 24, 30, 352, 350, "Food")
item2 = Item("plastron", 1, 10, 300, 450, "Plastron")
item3 = Item("apple", 24, 10, 352, 290, "Food")
item4 = Item("bottes", 1, 10, 500, 270, "Bottes")
item5 = Item("rubis", 24, 10, 352, 530, "Artefact")
item6 = Item("casque", 1, 10, 180, 560, "Casque")
item7 = Item("jambiere", 1, 10, 352, 230, "Jambiere")

item8 = Item("fish", 24, 10, 352, 710, "Food")
item9 = Item("pioche1", 24, 10, 352, 130, "Pioche")
item10 = Item("hache", 24, 10, 400, 130, "Hache")



# Création des arbres et ajout au groupe
trees = [Arbre("arbre", x, y) for x, y in tree_positions]


map_data = pyscroll.data.TiledMapData(tmx_data)

# Créer un groupe de rendu pour pyscroll
map_layer = pyscroll.orthographic.BufferedRenderer(map_data, screen.get_size())
map_layer.zoom = 2  # Facteur de zoom (1 = taille normale, 2 = zoomé x2)

# Créer un groupe de sprites avec caméra centrée
group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

# Ajoute les objets au groupe
group.add(player, layer=5)
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

#On ajoute ici le coffre
group.add(chest1,layer = 2)

#On ajoute ici les PNJ
group.add(pnj1 , layer = 2 )

#On ajoute ici les gobelins
group.add(gobelin1,layer = 2)
group.add(gobelin2,layer = 2)
group.add(gobelin3, layer = 2)
#group.add(pnj2, layer = 2)

group.add(slime1 ,layer = 2)
troncs = []
for x, y in tree_positions:
    feuillage = Feuillage(x, y)
    tronc = Tronc(x, y)
    tronc.feuillage = feuillage  # ← On associe le feuillage au tronc
    group.add(tronc, layer=2)
    group.add(feuillage, layer=6)
    troncs.append(tronc)  # ← On garde une liste de tous les troncs si besoin

# Fonction quit
def quit():
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    

# Fonction input pour gérer les entrées clavier
def input():
    pressed = pygame.key.get_pressed()
    dx, dy = 0, 0

    sprinting = pressed[pygame.K_r] and player.endurance_value > 0 and player.Regen == False  # Vérifie si le joueur peut sprinter

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

# Paramètres la progression du cercle pour le "manger"
fill_time = 3.0  # Durée du remplissage
fill_time_cut = 11
progress = 0.0
progressing = False
finished_time = 0
show_message = False

progress_cut = 0.0
cut_progressing = False
finished_time_cut = 0

# Booléens :
show_inventory = False  # booléen pour gérer l'affichage de l'inventaire
moving = True  # booléen pour gérer le droit de mouvement du personnage
eat_image = pygame.image.load("UI/soin1.png")



IsCursorOn = True

Arbre_touche = False

running = True
near_chest = None  # coffre à proximité par défaut à None



can_talk_to_pnj1 = False

active_pnj = None

while running:
    dt = mainClock.tick(60) / 1000  # Temps écoulé en secondes
    
    

    for event in pygame.event.get():
        quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                show_inventory = not show_inventory  # On inverse l'état de l'inventaire
                player.OnBag = True
                player.OnArmour = False
                moving = not moving
        

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if show_inventory == False:
                # Animation attaque
                if player.last_direction == "right" or player.last_direction == "down":
                    player.start_anim_attack(player.attack_right_mouv, 0.3, 0)
                if player.last_direction == "left" or player.last_direction == "up":
                    player.start_anim_attack(player.attack_left_mouv, 0.3, -0)

                # Vérifie l'attaque sur les ennemis
                for sprite in group.sprites():
                    if isinstance(sprite, Enemy):
                        # Créer une "zone d'attaque" autour du joueur
                        attack_zone = player.hit_box.inflate(40, 40)  # Zone légèrement plus grande
                        if attack_zone.colliderect(sprite.rect):
                            sprite.current_health -= 10  # Inflige 10 de dégâts
                            if player.last_direction == "right":
                                sprite.knockback = True
                                sprite.knockback_speed = 6
                                sprite.knockback_direction = 1

                            if player.last_direction == "left":
                                sprite.knockback = True
                                sprite.knockback_speed = 6
                                sprite.knockback_direction = -1

                            if sprite.current_health < 0:
                                sprite.current_health = 0
                            if sprite.current_health == 0:
                                group.remove(sprite)
                
            

            if player.rect_button_armour.collidepoint(event.pos):
                player.OnArmour = True
                player.OnBag = False
            if player.rect_button_bag.collidepoint(event.pos):
                player.OnArmour = False
                player.OnBag = True
            if player.rect_button_book.collidepoint(event.pos):
                show_inventory = False
                player.OnBook = True
                player.startBookAnimation(player.open_book, 0.3)  

            if player.rect_button_back_book.collidepoint(event.pos):
                player.OnBook = False
                moving = True
                player.current_book_index = 0
                player.IsAnimating = True
                player.IsOpen = False

            if player.rect_button_left_book.collidepoint(event.pos) and player.page > 0:
                player.startBookAnimation(player.turn_left, 0.25)
                
                player.IsOpen = True
                player.page_a_cote = player.page - 1
                player.page -= 2

            if player.rect_button_right_book.collidepoint(event.pos) and player.page < 20:
                player.startBookAnimation(player.turn_right, 0.25)
                player.IsOpen = True
                player.page += 2
                player.page_a_cote = player.page + 1

        if show_inventory:
            player.handle_mouse_events(event)

        player.handle_key_events(event)

        save_menu.handle_event(event,"ruen",1,player.rect.x,player.rect.y)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                if near_chest and near_chest.Can_open:
                    near_chest.start_animation_coffre(near_chest.coffre_open_list, 0.3)
                elif active_pnj:  # ← Si on a un PNJ actif
                    active_pnj.CanDialog = not active_pnj.CanDialog
                    if active_pnj.CanDialog:
                        active_pnj.start_dialog(0)  # ← Lancer le texte de ce PNJ
            if event.key == pygame.K_SPACE:
                if active_pnj and active_pnj.CanDialog:
                    active_pnj.next_dialog()






                    

       
    # vérifier si l'on peut marcher
    if moving:
        input()

    player.anim_player_full_animation()

    if show_inventory == False:
        # Clic droit maintenu pour gérer l'affichage du "progress circle"
        if player.inventory_bar_list[player.inventory_index] != {}:
            if player.inventory_bar_list[player.inventory_index]['object'].type == "Food":
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
                                
                                player.eat(player.inventory_index)  # On active la méthode eat lorsque "la progress circle" se termine
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

    if player.OnBook:
        player.animBook()

    if progressing:
        world_pos = (player.rect.centerx , player.rect.top - 10)
        screen_pos = map_layer.translate_point(world_pos)

        radius = 30
        end_angle = -math.pi / 2 + progress * 2 * math.pi
        pygame.draw.circle(screen, (100, 100, 100), screen_pos, radius, 3)
        pygame.draw.arc(screen, (0, 200, 0), (screen_pos[0] - radius, screen_pos[1] - radius, radius * 2, radius * 2),
                        -math.pi / 2, end_angle, 4)

        screen.blit(eat_image, (screen_pos[0] - 30, screen_pos[1] - 27))
        
    if player.inventory_bar_list[player.inventory_index] != {}:
        if player.inventory_bar_list[player.inventory_index]['object'].type == "Hache":
            fill_time_cut = 4
        else:
            fill_time_cut = 8
    near_chest = None  # Reset à chaque frame
    
    for sprite in group.sprites():
        if show_inventory == False:
            if isinstance(sprite, Tronc) and player.hit_box.colliderect(sprite.hitbox):
                
                if sprite.Can_cut:
                    if pygame.mouse.get_pressed()[0]:
                        if not cut_progressing:
                            cut_progressing = True
                            progress_cut = 0.0
                        else:
                            progress_cut += dt / fill_time_cut

                            if player.inventory_bar_list[player.inventory_index] != {}:
                                if player.inventory_bar_list[player.inventory_index]['object'].type == "Hache":
                                    player.animation_hache(player.hache_anim, 1.5)

                            if progress_cut >= 1.0:
                                cut_progressing = False
                                if hasattr(sprite, 'feuillage'):
                                    group.remove(sprite.feuillage)  # ← On supprime le feuillage lié
                                group.add(Item("buche1", 24, 10, sprite.rect.x + 50, sprite.rect.y + 50, "Food"))
                                group.add(Item("buche1", 24, 10, sprite.rect.x + 30, sprite.rect.y + 30, "Food"))
                                group.add(Item("buche1", 24, 10, sprite.rect.x + 20, sprite.rect.y + 50, "Food"))
                                if choice([1,2,3,4,5,6,7,8,9,10]) == 1:
                                    group.add(Item("apple", 24, 10, sprite.rect.x + 20, sprite.rect.y + 10, "Food"))
                                    
                                sprite.image = pygame.image.load("Objects/souche.png")
                                sprite.hitbox = sprite.rect.copy().inflate(-63, -130)
                                sprite.hitbox.y +=55
                                sprite.Can_cut = False
                                finished_time_cut = pygame.time.get_ticks()
                    else:
                        if progress_cut < 1.0:
                            cut_progressing = False
                            progress_cut = 0.0

                    if cut_progressing:
                        world_pos = (player.rect.centerx, player.rect.top - 10)
                        screen_pos = map_layer.translate_point(world_pos)

                        radius = 60
                        end_angle = -math.pi / 2 + progress_cut * 2 * math.pi
                        pygame.draw.circle(screen, (100, 100, 100), screen_pos, radius, 3)
                        pygame.draw.arc(screen, (255, 140, 0), (screen_pos[0] - radius, screen_pos[1] - radius, radius * 2, radius * 2),
                                        -math.pi / 2, end_angle, 4)

                        if player.inventory_bar_list[player.inventory_index] != {}:
                            if player.inventory_bar_list[player.inventory_index]['object'].type == "Hache":
                                screen.blit(player.hache, (screen_pos[0] - 80, screen_pos[1] - 75))

            
        if isinstance(sprite, Tronc) and player.feet.colliderect(sprite.hitbox):
            player.move_back()

    

    #On gere ici les collision aves les objets de type "Coffre"
        if isinstance(sprite, Coffre) and player.feet.colliderect(sprite.rect):
            
            player.move_back()

        if isinstance(sprite, Coffre) and player.hit_box.colliderect(sprite.rect):
            near_chest = sprite  # On garde en mémoire le coffre à proximité
            if sprite.Can_open:
                world_pos = (player.rect.centerx , player.rect.top - 10)
                screen_pos = map_layer.translate_point(world_pos)
                screen.blit(player.key_board_I, (screen_pos[0]-23, screen_pos[1]+10))

        if isinstance(sprite, Item) and player.hit_box.colliderect(sprite.rect):
            group.remove(sprite)  # Supprime l'objet du groupe
            player.add_to_inventory(sprite)

        if isinstance(sprite, Entity) and player.feet.colliderect(sprite.hit_box):
            player.move_back()

        if isinstance(sprite, PNJ):
            if player.hit_box.colliderect(sprite.champ_vision):
                can_talk_to_pnj1 = True
                active_pnj = sprite  # ← Le PNJ actif devient celui détecté
                world_pos = (player.rect.centerx , player.rect.top - 10)
                screen_pos = map_layer.translate_point(world_pos)
                screen.blit(player.key_board_I, (screen_pos[0]-23, screen_pos[1]+10))
            else:
                if active_pnj == sprite:
                    sprite.CanDialog = False   # On FERME la boîte de dialogue
                    active_pnj = None
        if isinstance(sprite, Enemy):
            sprite.champ_vision_enemy.center = sprite.rect.center  # Toujours mettre à jour le champ de vision
            sprite.follow_player(player)

            # Si knockback est actif
            if sprite.knockback:
                sprite.rect.x += sprite.knockback_direction * sprite.knockback_speed
                sprite.knockback_speed -= 0.5  # on ralentit progressivement
                if sprite.knockback_speed <= 0:
                    sprite.knockback = False
                    sprite.knockback_speed = 0

            sprite.draw_health_bar(screen,map_layer)
        if isinstance(sprite,Slime):
            sprite.follow_player(player)
                    
           


       
            
            

    # Collision avec la map (rectangles Tiled)
    for rect in collision_rects:
        if player.feet.colliderect(rect):
            player.move_back()
            
    
                

    
    if show_inventory:
        player.display_inventory()  # On appelle la méthode display_inventory pour afficher l'inventaire

    if save_menu.quitte:
        moving = False
    else: 
        moving = True

    '''
    # Affichage optionnel des hitbox bour le debbugage
    pygame.draw.rect(screen, (255, 0, 0), map_layer.translate_rect(player.hit_box), 2)

    pygame.draw.rect(screen, (255, 255, 0), map_layer.translate_rect(player.feet), 2)
    for i in troncs:
        pygame.draw.rect(screen, (255, 0, 255), map_layer.translate_rect(i.hitbox), 2)

    pygame.draw.rect(screen, (255, 255, 0), map_layer.translate_rect(player.rect), 2)
    
    for i in collision_rects:
        pygame.draw.rect(screen, (255, 255, 0), map_layer.translate_rect(i), 2)
    

    pygame.draw.rect(screen, (255, 255, 0), map_layer.translate_rect(chest1.rect), 2)
    pygame.draw.rect(screen, (255, 255, 0), map_layer.translate_rect(player.feet), 2)

    pygame.draw.rect(screen, (255, 125, 56), map_layer.translate_rect(pnj1.rect), 2)
    pygame.draw.rect(screen, (255, 0, 0), map_layer.translate_rect(player.hit_box), 2)
    pygame.draw.rect(screen, (255, 125, 56), map_layer.translate_rect(pnj1.champ_vision), 2)
    pygame.draw.rect(screen, (255, 125, 56), map_layer.translate_rect(gobelin1.champ_vision_enemy), 2)
    print(a_proximite)
    '''
    pygame.draw.rect(screen, (255, 125, 56), map_layer.translate_rect(slime1.champ_vision_enemy), 2)

    pnj1.update()
    
    save_menu.update()
    chest1.anim_chest()
    
    
    pnj1.idle()
    

    pygame.display.update()
