
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
        else:
            print(f"Could not place tree {len(positions) + 1} after {max_attempts} attempts.")
    return positions

# Generate positions for 30 trees with a minimum distance of 100 pixels
#tree_positions = [(216, 860), (1430, 1322), (1026, 1471), (20, 537), (899, 706), (1332, 1150), (1124, 395), (698, 252), (816, 18), (1513, 1237), (327, 119), (479, 1026), (613, 619),(114,1460),(298,1460)]
tree_positions = generate_tree_positions(1560, 1530, 30, 40)

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
from arbre_Yahya import *

pygame.init()
pygame.display.set_caption("Jeu")

# Définition de la fenêtre
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Chargement de la carte Tiled
tmx_data = load_pygame("maps/maps.tmx")  # Remplace par ton fichier .tmx

player_position = tmx_data.get_object_by_name("Player")
player = Player(player_position.x, player_position.y, screen)  # Positionner le joueur

item = Item("pain", 24, 10, 352, 350, "Food")
item2 = Item("plastron", 1, 10, 300, 450, "Plastron")
item3 = Item("apple", 24, 10, 352, 290, "Food")
item4 = Item("bottes", 1, 10, 500, 270, "Bottes")
item5 = Item("fromage", 24, 10, 330, 500, "Food")
item6 = Item("rubis", 24, 10, 352, 530, "Artefact")
item7 = Item("casque", 1, 10, 180, 560, "Casque")
item8 = Item("jambiere", 1, 10, 352, 230, "Jambiere")
item9 = Item("pain", 24, 10, 352, 700, "Food")
item10 = Item("fish", 24, 10, 352, 710, "Food")
item11 = Item("fromage", 24, 10, 352, 130, "Food")
item12 = Item("hache", 24, 10, 400, 130, "Hache")
item13 = Item("emeraude", 24, 10, 408, 110, "Artefact")



# Création des arbres et ajout au groupe
trees = [Arbre("arbre", x, y) for x, y in tree_positions]

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

# Ajoute les arbres au groupe
for tree in trees:
    group.add(tree)

# Fonction quit
def quit():
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.KEYDOWN:  # Si une touche est pressée
        if event.key == pygame.K_ESCAPE:  # Si la touche pressée est "Échap"
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

curent_quantity = 0

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

curseur = pygame.image.load("UI/curseur1.png")
curseur_rect = curseur.get_rect()

IsCursorOn = True

Arbre_touche = False
while True:
    dt = mainClock.tick(60) / 1000  # Temps écoulé en secondes
    pygame.mouse.set_visible(False)
    curseur_rect.topleft = pygame.mouse.get_pos()

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
                if player.last_direction == "right" or player.last_direction == "down":
                    player.start_anim_attack(player.attack_right_mouv, 0.3, 0)

                if player.last_direction == "left" or player.last_direction == "up":
                    player.start_anim_attack(player.attack_left_mouv, 0.3, -0)

            if player.rect_button_armour.collidepoint(event.pos):
                player.OnArmour = True
                player.OnBag = False
            if player.rect_button_bag.collidepoint(event.pos):
                player.OnArmour = False
                player.OnBag = True
            if player.rect_button_book.collidepoint(event.pos):
                show_inventory = False
                player.OnBook = True
                player.startBookAnimation(player.open_book, 0.3)  # Assurez-vous que cette ligne est présente

            if player.rect_button_back_book.collidepoint(event.pos):
                player.OnBook = False
                moving = True
                player.current_book_index = 0
                player.IsAnimating = True
                player.IsOpen = False

            if player.rect_button_left_book.collidepoint(event.pos) and player.page > 0:
                player.startBookAnimation(player.turn_left, 0.25)
                print("bouton clique")
                player.IsOpen = True
                player.page_a_cote = player.page - 1
                player.page -= 2

            if player.rect_button_right_book.collidepoint(event.pos) and player.page < 6:
                player.startBookAnimation(player.turn_right, 0.25)
                player.IsOpen = True
                print("bouton clique")
                player.page += 2
                player.page_a_cote = player.page + 1

        if show_inventory:
            player.handle_mouse_events(event)

        player.handle_key_events(event)

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
                                print("Nourriture consommée")
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
        world_pos = (player.rect.centerx + 25, player.rect.top - 10)
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

    for sprite in group.sprites():
        if show_inventory == False:
            if isinstance(sprite, Arbre) and player.rect.colliderect(sprite.rect):
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
                            group.add(Item("buche1", 24, 10, sprite.rect.x + 50, sprite.rect.y + 50, "Food"))
                            group.add(Item("buche1", 24, 10, sprite.rect.x + 30, sprite.rect.y + 30, "Food"))
                            group.add(Item("buche1", 24, 10, sprite.rect.x + 20, sprite.rect.y + 50, "Food"))
                            group.remove(sprite)
                            finished_time_cut = pygame.time.get_ticks()
                else:
                    if progress_cut < 1.0:
                        cut_progressing = False
                        progress_cut = 0.0

                if cut_progressing:
                    world_pos = (player.rect.centerx + 25, player.rect.top - 10)
                    screen_pos = map_layer.translate_point(world_pos)

                    radius = 60
                    end_angle = -math.pi / 2 + progress_cut * 2 * math.pi
                    pygame.draw.circle(screen, (100, 100, 100), screen_pos, radius, 3)
                    pygame.draw.arc(screen, (0, 200, 0), (screen_pos[0] - radius, screen_pos[1] - radius, radius * 2, radius * 2),
                                    -math.pi / 2, end_angle, 4)

                    if player.inventory_bar_list[player.inventory_index] != {}:
                        if player.inventory_bar_list[player.inventory_index]['object'].type == "Hache":
                            screen.blit(player.hache, (screen_pos[0] - 80, screen_pos[1] - 75))

    for sprite in group.sprites():
        if isinstance(sprite, Item) and player.rect.colliderect(sprite.rect):
            group.remove(sprite)  # Supprime l'objet du groupe
            player.add_to_inventory(sprite)

    if show_inventory:
        player.display_inventory()  # On appelle la méthode display_inventory pour afficher l'inventaire

    screen.blit(curseur, curseur_rect)

    pygame.display.update()
