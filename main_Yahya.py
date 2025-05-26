
import random
from quete_principales_final import *
def generate_tree_positions(max_x, max_y, num_trees, min_distance, max_attempts=1000):
    positions = list()
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
tree_positions = [(988, 1664), (186, 43), (270, 979), (790, 1323), (492, 2135), (898, 791), (327, 370), (1149, 1163), (1426, 1594), (397, 192), (1235, 1442), (747, 2010), (28, 2318), (688, 1731), (1072, 1542), (1573, 279), (1190, 2062), (445, 1894), (557, 1953), (1304, 488), (89, 1278), (1509, 1039), (603, 329), (944, 533), 
                  (1358, 850), (143, 731), (1467, 893), (647, 131), (227, 649), (1029, 234)]

print(generate_tree_positions(1585,2381,35,40))


import pygame, sys
import pytmx
from pytmx.util_pygame import load_pygame
import pytmx.util_pygame
from player_Yahya import *
from items import *

from pygame.locals import *
import pyscroll
import pyscroll.data
import time
from objects_Yahya import *
from random import *
pygame.init()
pygame.key.set_repeat(400, 20)  # délai initial 400ms, puis 40ms entre répétitions
pygame.display.set_caption("The Last Heir")
from scripte.save_game_yahya import*

import pygame
from classe_entity_Yahya import *
from dialog_data import *

from login_class import *
import networkx as nx
from classe_book_yahya import *


# Création du graphe dirigé
graphe_quetes = nx.DiGraph()

# Création des objets quête
q1 = Quete("Q1", "Trouver le coffre", "Suivez le chemin et trouvez le coffre.")
q2 = Quete("Q2", "Trouver le guide", "Trouver le guide dans le bois.")

q3 = Quete("Q3", "Ramasser du bois", "Ramasser 10 buches dans la forêt.")
q4 = Quete("Q4","Récupérer des pommes","Ramasser 5 pommes dans la foret.")
q5 = Quete("Q5","Retrouver le vieux guide","Retrouver le vieux guide.")
q6 = Quete("Q6","Trouver le portail","Rejoignez le portail pour le monde \n principal.")
q7 = Quete("Q7","trouver le maire de Grotval","Trouver le maire de Grotval, \n le village des mineurs.)")
# Ajout des nœuds avec attributs
graphe_quetes.add_node("Q1", quete=q1)
graphe_quetes.add_node("Q2", quete=q2)
graphe_quetes.add_node("Q3", quete=q3)
graphe_quetes.add_node("Q4",quete = q4)
graphe_quetes.add_node("Q5",quete = q5)
graphe_quetes.add_node("Q6",quete = q6 )
graphe_quetes.add_node("Q7",quete = q7 )
# Ajout des relations (choix ou dépendances)
graphe_quetes.add_edge("Q1", "Q2")  # Après Q1, Q2 est possible
graphe_quetes.add_edge("Q2", "Q3",choix=True)  # Après Q2, Q3 est possible
graphe_quetes.add_edge("Q2","Q4",choix=True)     # Après Q2, Q4 est possible
graphe_quetes.add_edge("Q3","Q5")
graphe_quetes.add_edge("Q4","Q5")
graphe_quetes.add_edge("Q5","Q6")
graphe_quetes.add_edge("Q6","Q7")

#variable username utilisé pour stocké le pseudo du joueur
username = ""

font = pygame.font.Font("Items/Minecraft.ttf", 14)
def verification(username,password):
    """
        Fonction de vérification du login
        attribut:
            username : pseudo du joueur
            password : mot de passe du joueur
    """
    pannel_create_an_account = pygame.image.load("UI/create_account.png")
    x_pannel_create_an_account = screen.get_width() // 2 - pannel_create_an_account.get_width() // 2
    y_pannel_create_an_account = screen.get_height()//2 - pannel_create_an_account.get_height()//2
    
    font = pygame.font.Font("UI/dialog_font.ttf", 15)
    message_erreur = font.render("Identifiant/Mot de passe invalide", True, (255, 0, 0))

    # Connexion à la base de données SQLite
    conn = sqlite3.connect('database/data_yahya.db')
    cursor = conn.cursor()

    # Requête pour vérifier si le nom d'utilisateur et le mot de passe existent dans la table "users"
    cursor.execute('''SELECT pseudo,password FROM Login WHERE pseudo=? AND password=?;''', (username, password))
    result = cursor.fetchall()

    # Fermer la connexion à la base de données
    conn.close()

    if result:
        return True  # Identifiant et mot de passe valides
    else : 
        return False # Identifiant ou mot de passe invalide
    

def create_account(username,password,confirm_password):
    """
        Fonction de création de compte
        Attribut :
            username : pseudo du joueur
            password : mot de passe du joueur
            confirm_password : mot de passe de confirmation du joueur
    """
    pannel_create_an_account = pygame.image.load("UI/create_account.png")
    x_pannel_create_an_account = screen.get_width() // 2 - pannel_create_an_account.get_width() // 2
    y_pannel_create_an_account = screen.get_height()//2 - pannel_create_an_account.get_height()//2

    tmx_data = load_pygame("maps/map_tuto.tmx")  
    player_position = tmx_data.get_object_by_name("Player")
    id_quete_deBase = "Q1"
    if username == "" or password == "" or confirm_password == "":
        font = pygame.font.Font("UI/dialog_font.ttf", 15)
        message_erreur = font.render("Veuiller insérer un identifiant et un mot de passe", True, (255, 0, 0))
        screen.blit(message_erreur, (x_pannel_create_an_account ,y_pannel_create_an_account))
        pygame.display.update()
        pygame.time.delay(2000)
        print("rien")
        return
    
    conn = sqlite3.connect('database/data_yahya.db')
    cursor = conn.cursor()
    # Requête pour vérifier si le nom d'utilisateur existe déjà dans la table "users"
    cursor.execute('''SELECT pseudo FROM Login WHERE pseudo=?;''', (username,))
    result = cursor.fetchall()
    if result != []:
                cursor.close()
                conn.commit()
                conn.close()
                font = pygame.font.Font("UI/dialog_font.ttf", 15)
                message_erreur = font.render("Pseudo déjà existant", True, (255, 0, 0))
                screen.blit(message_erreur, (x_pannel_create_an_account ,y_pannel_create_an_account))
                pygame.display.update()
                pygame.time.delay(2000)
                print("pseudo déjà existant")
                return
        

    if username != "" and password != "" and confirm_password != "" and result == [] :
        if password == confirm_password:
            # Connexion à la base de données SQLite
            conn = sqlite3.connect('database/data_yahya.db')
            cursor = conn.cursor()
            # Requête pour stocker le nom d'utilisateur et le mot de passe dans la table "users"
            cursor.execute('''INSERT INTO Login (pseudo,password,pos_x,pos_y,health,mana,endurance,level,current_quete,current_map) values (?,?,?,?,100,0,100,0,?,"map_tuto") ''',(username,password,player_position.x,player_position.y,id_quete_deBase))
            cursor.execute('''INSERT INTO Coffre (chest_name,chest_index,pseudo) values ("coffre1",0,?) ''',(username,))
            cursor.close()
            conn.commit()
            conn.close()
            return True  # Identifiant et mot de passe valides
            
            
        else : 
            font = pygame.font.Font("UI/dialog_font.ttf", 15)
            message_erreur = font.render("Les mots de passe ne correspondent pas", True, (255, 0, 0))
            screen.blit(message_erreur, (x_pannel_create_an_account ,y_pannel_create_an_account))
            pygame.display.update()
            pygame.time.delay(2000)  # Affiche le message pendant 2 secondes
            print("mdp diff")
            return
    

def login():

    global username
    button_sfx = pygame.mixer.Sound("music/button1.mp3")
    Login = True
    Confirm = False
    background_image = pygame.image.load("UI/bg_menu.png")
    background_image = pygame.transform.scale(background_image, screen.get_size())
    logo_image = pygame.image.load("UI/Logo.png")

    pannel_create_an_account = pygame.image.load("UI/create_account.png")
    x_pannel_create_an_account = (screen.get_width() - pannel_create_an_account.get_width()) // 2
    y_pannel_create_an_account = (screen.get_height() - pannel_create_an_account.get_height())//2
    #Ajout du boutton quitter
    quit_button = pygame.image.load("UI/quitter_account.png.png")
    rect_quit_button = quit_button.get_rect()
    x_quit = screen.get_width()-rect_quit_button.width - 10 # 10 pixels de marge à droite
    y_quit = 0 + rect_quit_button.height - 10 # 10 pixels de marge en bas
    rect_quit_button.x = x_quit
    rect_quit_button.y = y_quit
    #coordonnée de bases
    x =screen.get_width()//2 -220
    y= screen.get_height()//2 - 47

    #définition des input box de la création 
    username_box1 = InputBox(x_pannel_create_an_account + 125, y_pannel_create_an_account+128, 270, 30)
    password_box1 = InputBox(x_pannel_create_an_account + 125, y_pannel_create_an_account+223, 270, 30, is_password=True)
    confirm_password_box1 = InputBox(x_pannel_create_an_account + 125, y_pannel_create_an_account+313, 270, 30, is_password=True)

    #définitions des input box du login 
    username_box = InputBox(x + 93, y + 123, 200, 30)
    password_box = InputBox(x + 93, y + 200, 200, 30, is_password=True)

    #ajout icone pour le mot de passe oeuil ouvert oeil fermé
    oeil_ouvert1 = pygame.image.load("UI/oeil_ouvert.png")
    oeil_ouvert1 = pygame.transform.scale(oeil_ouvert1,(50,50))
    rect_oeil_ouvert1 = oeil_ouvert1.get_rect(topleft=(x + 333, y + 190))
    
    oeil_ouvert2 = pygame.image.load("UI/oeil_ouvert.png")
    oeil_ouvert2 = pygame.transform.scale(oeil_ouvert2,(50,50))
    rect_oeil_ouvert2 = oeil_ouvert2.get_rect(topleft=(x_pannel_create_an_account + 400, y_pannel_create_an_account+213))
    
    oeil_ouvert3 = pygame.image.load("UI/oeil_ouvert.png")
    oeil_ouvert3 = pygame.transform.scale(oeil_ouvert3,(50,50))
    rect_oeil_ouvert3 = oeil_ouvert3.get_rect(topleft=(x_pannel_create_an_account + 400, y_pannel_create_an_account+303))

    oeil_ferme = pygame.image.load("UI/oeil_fermé.png")
    oeil_ferme = pygame.transform.scale(oeil_ferme,(50,50))

    retour_image = pygame.image.load("UI/retour_account.png")
    rect_retour_image = retour_image.get_rect(topleft=(20,rect_quit_button.height - 10))
    Can_see_password = False
    font = pygame.font.Font("UI/dialog_font.ttf", 15)
    message_erreur = font.render("Les mots de passe ne correspondent pas", True, (255, 0, 0))


    # rectangle de création de compte
    btn_create_account = pygame.Rect(x_pannel_create_an_account + 153, y_pannel_create_an_account + 363, 181, 52)
    
    if Login:
        logo_image = pygame.transform.scale(logo_image, (600, 600))
        
        

        rect = pygame.Rect(x + 122, y + 247, 181, 52)
        
        pannel = pygame.image.load("UI/loginv2.png.png")
        rect_pannel = pannel.get_rect()
        rect_pannel.x = x
        rect_pannel.y = y
        x_pannel_login = (screen.get_width() - pannel.get_width()) // 2
        y_pannel_login = (screen.get_height() - pannel.get_height())//2
        
        #panneau création de compte
        pannel_create = pygame.image.load("UI/creer_compte_pannel.png")
        
        #bouton de création de compte 
        btn_creation = pygame.image.load("UI/btn_cr.png")
        btn_creation = pygame.transform.scale(btn_creation,(250,65))
        rect_btn_creation = btn_creation.get_rect()
        x_btn_creation = x + 80
        y_btn_creation = y+ pannel.get_height() + 15
        rect_btn_creation.x = x_btn_creation
        rect_btn_creation.y = y_btn_creation
        rect_creer_compte = pygame.Rect(rect_btn_creation.x,rect_btn_creation.y,rect_btn_creation.width,rect_btn_creation.height)
        

        #screen.blit(message_erreur, (x_pannel_create_an_account , y_pannel_create_an_account))
        
    if Confirm:
        logo_image = pygame.transform.scale(logo_image, (300, 300))

        
        

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                if Login:
                    if rect.collidepoint(event.pos):
                        if verification(username_box.text, password_box.text):
                            running = False
                            username = username_box.text
                            print("Login successful")
                            return
                        else:
                            ## revoie un message d'erreur si le login est incorrect
                            font = pygame.font.Font("UI/dialog_font.ttf", 12)
                            error_message = font.render("Identifiant ou mot de passe invalide", True, (255, 0, 0))
                            screen.blit(error_message, (x, y + 50))
                            pygame.display.update()
                            pygame.time.delay(2000)  # Affiche le message pendant 2 secondes
                            username_box.text = ""
                            password_box.text = ""
                        
                        
                    if rect_creer_compte.collidepoint(event.pos):
                        Login = False
                        Confirm = True
                        button_sfx.play()
                        
                    if rect_oeil_ouvert1.collidepoint(event.pos):
                        if Can_see_password == False:
                            password_box.set_password_mode(False)  # ou False
                            Can_see_password = True
                            oeil_ouvert1 = oeil_ferme
                            button_sfx.play()
                        else:
                            password_box.set_password_mode(True)
                            Can_see_password = False
                            oeil_ouvert1 = pygame.image.load("UI/oeil_ouvert.png")
                            oeil_ouvert1 = pygame.transform.scale(oeil_ouvert1,(50,50))
                if Confirm:

                    if rect_oeil_ouvert2.collidepoint(event.pos):
                        if Can_see_password == False:
                            password_box1.set_password_mode(False)  # ou False
                            Can_see_password = True
                            oeil_ouvert2 = oeil_ferme
                            button_sfx.play()
                        else:
                            password_box1.set_password_mode(True)
                            Can_see_password = False
                            oeil_ouvert2 = pygame.image.load("UI/oeil_ouvert.png")
                            oeil_ouvert2 = pygame.transform.scale(oeil_ouvert1,(50,50)) 
                    if rect_oeil_ouvert3.collidepoint(event.pos):
                        if Can_see_password == False:
                            confirm_password_box1.set_password_mode(False)  # ou False
                            Can_see_password = True
                            oeil_ouvert3 = oeil_ferme
                            button_sfx.play()
                        else:
                            confirm_password_box1.set_password_mode(True)
                            Can_see_password = False
                            oeil_ouvert3 = pygame.image.load("UI/oeil_ouvert.png")
                            oeil_ouvert3 = pygame.transform.scale(oeil_ouvert1,(50,50))
                    if rect_retour_image.collidepoint(event.pos):
                        button_sfx.play()
                        Login = True
                        Confirm = False
                    if btn_create_account.collidepoint(event.pos):
                        button_sfx.play()
                        
                        #if create_account(username_box1.text,password_box1.text,confirm_password_box1.text) == "rien":
                            
                            
                        
                        #if create_account(username_box1.text,password_box1.text,confirm_password_box1.text) == "pseudo déjà existant":
                            

                        #if create_account(username_box1.text,password_box1.text,confirm_password_box1.text) == "mot de passe différent": 
                            

                        if create_account(username_box1.text,password_box1.text,confirm_password_box1.text):
                            print("Login successful")
                            running = False
                            username = username_box1.text
                            return
                        

            if Login:
                username_box.handle_event(event)
                password_box.handle_event(event)
            if Confirm:
                username_box1.handle_event(event)
                password_box1.handle_event(event)
                confirm_password_box1.handle_event(event)


        # Affichage du background
        screen.blit(background_image, (0, 0))
        screen.blit(quit_button, rect_quit_button)
        
        if Login:
            logo_image = pygame.transform.scale(logo_image, (600, 600))

            screen.blit(logo_image, (screen.get_width() // 2 - logo_image.get_width() // 2,-80))
            screen.blit(pannel,rect_pannel)
            
            screen.blit(btn_creation, rect_btn_creation)
            
            username_box.draw(screen)
            username_box.update_cursor()
            password_box.draw(screen)
            password_box.update_cursor()
            screen.blit(oeil_ouvert1, rect_oeil_ouvert1)    
            
        if Confirm:
            logo_image = pygame.transform.scale(logo_image, (300, 300))
            screen.blit(logo_image, (screen.get_width() // 2 - logo_image.get_width() // 2,-50))
            screen.blit(pannel_create_an_account, (x_pannel_create_an_account,y_pannel_create_an_account))
            username_box1.draw(screen)
            username_box1.update_cursor()
            password_box1.draw(screen)
            password_box1.update_cursor()
            confirm_password_box1.draw(screen)
            confirm_password_box1.update_cursor()

            screen.blit(oeil_ouvert2, rect_oeil_ouvert2)
            screen.blit(oeil_ouvert3, rect_oeil_ouvert3)
            screen.blit(retour_image, rect_retour_image)
            
        pygame.display.flip()

# Définition de la fenêtre
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 

run = False

# fonction pour afficher le menu principal
def main_menu():
    global run,username
    
    WHITE = (255, 255, 255)
    GRAY = (100, 100, 100)

    retour_image = pygame.image.load("UI/retour_account.png")
    rect_retour_image = retour_image.get_rect(topleft=(0,0))

    background_image = pygame.image.load("UI/bg_menu.png")
    background_image = pygame.transform.scale(background_image, screen.get_size())
    button_bg = pygame.image.load("UI/button_play.png")
    button_bg = pygame.transform.scale(button_bg, (300, 93))
    #Image du Logo
    game_logo = pygame.image.load("UI/Logo.png")
    game_logo = pygame.transform.scale(game_logo,(600,600))
    #Police d'écriture
    button_font = pygame.font.Font("UI/dialog_font.ttf", 45)
    username_font = pygame.font.Font("UI/dialog_font.ttf", 25)

    #création des textes
    play_text = button_font.render("LAUNCH GAME", True, WHITE)
    credits_text = button_font.render("CREDITS", True, WHITE)
    quit_text = button_font.render("EXIT", True, WHITE)

    # Obtenir les dimensions du texte
    play_width, play_height = play_text.get_size()
    
    #Obtention des dimensions du logo
    logo_width,logo_height = game_logo.get_size()

    # Calculer la position pour placer le texte en bas à droite
    x = 100
    y = 0 + logo_height -100  # 70 pixels de marge en bas 

    # Obtenir les dimensions du texte
    quit_width, quit_height = play_text.get_size()
    
    #On charge ici l'image du profil 
    profile_image = pygame.image.load("UI/profile_white2.png")
    #on créer ici le texte du username
    username_text = username_font.render(username, True, WHITE)

    # Calculer la position pour placer le texte en bas à droite
    x_quit = screen.get_width() - quit_width - 10  # 10 pixels de marge à droite
    y_quit = 0 + quit_height - 10  # 10 pixels de marge en bas
    
    play_rect = play_text.get_rect()
    play_rect.x = x
    play_rect.y = y

    quit_rect = quit_text.get_rect()
    quit_rect.x = x
    quit_rect.y = y +200
    credits_rect = credits_text.get_rect(center=(x,y +100))
    credits_rect.x = x
    credits_rect.y = y + 100
    
    player_idle = Player(0, 0, screen)
    player_idle.image = pygame.transform.scale(player_idle.image, (400, 400))
    player_idle.rect.center = (screen.get_width() // 2-100, screen.get_height() // 2- 105)
    
    
    running_menu = True
    sprites = pygame.sprite.Group()
    skin = Player(100, 100, screen) 
    sprites.add(skin)


    font = pygame.font.Font("UI/dialog_font.ttf", 30)
    credits = [
        "Un jeu développé par Yahya et Ayyoub",
        "Grafics YahyouSyle ",
        "Musique Pixabay",
        "Remerciements spéciaux à :",
        "Albin, Mr Martin alias Philipus Martinus",
        "(qui ne goutera qu'a 2% des bénéfices si on n'a pas 20)",
        "A Raph aussi",
        "A Tchoupi",
        "et au PNJ",
        "Un jeu fait avec Pygame",
        "2025",
        "Realease le 15 juillet 2025 ",
        "The Last Heir ©"

    ]

    # Créer un grand texte à défiler
    lines = [font.render(line, True, (255, 255, 255)) for line in credits]
    total_height = sum(line.get_height() + 20 for line in lines)
    start_y = screen.get_height()

    Acceuil = True
    Credits = False
    Music = True
    button_sfx = pygame.mixer.Sound("music/button1.mp3")

   
    pygame.mixer.music.load("music/music.mp3")
    pygame.mixer.music.set_volume(0.5)  # 0.0 (muet) à 1.0 (volume max)
    pygame.mixer.music.play(-1)  # Joue la musique en boucle
    print("Musique lancée")
    while running_menu:
        mouse_pos = pygame.mouse.get_pos()
        
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    button_sfx.play()
                    pygame.mixer.music.pause()
                    launch_game()
                    pygame.event.clear()
                    

                elif quit_rect.collidepoint(event.pos):
                    button_sfx.play()
                    pygame.quit()
                    sys.exit()
                elif credits_rect.collidepoint(event.pos):
                    button_sfx.play()
                    Credits = True
                    Acceuil = False
                elif rect_retour_image.collidepoint(event.pos):
                    button_sfx.play()
                    Credits = False
                    Acceuil = True
        screen.blit(background_image, (0, 0))
        
        if Acceuil:
            screen.blit(game_logo,(0,-80))

            # Détection du hover
            play_color = GRAY if play_rect.collidepoint(mouse_pos) else WHITE
            quit_color = GRAY if quit_rect.collidepoint(mouse_pos) else WHITE
            credits_color = GRAY if credits_rect.collidepoint(mouse_pos) else WHITE
            #création des textes
            play_text = button_font.render("LAUNCH GAME", True, play_color)
            credits_text = button_font.render("CREDITS", True, credits_color)
            quit_text = button_font.render("EXIT", True, quit_color)
            
            # Ombre
            shadow_offset = (5, 2)
            play_shadow = button_font.render("LAUNCH GAME", True, (0, 0, 0))  # ombre noire
            screen.blit(play_shadow, (play_rect.x + shadow_offset[0], play_rect.y + shadow_offset[1]))
            screen.blit(play_text, play_rect)
            #Affichage bouton quitter avec ombre
            quit_shadow = button_font.render("EXIT", True, (0, 0, 0))
            screen.blit(quit_shadow, (quit_rect.x + shadow_offset[0], quit_rect.y + shadow_offset[1]))
            screen.blit(quit_text, quit_rect)

            #Affichage bouton credits avec ombre
            credits_shadow = button_font.render("CREDITS", True, (0, 0, 0))
            screen.blit(credits_shadow, (credits_rect.x + shadow_offset[0], credits_rect.y + shadow_offset[1]))
            screen.blit(credits_text, credits_rect)

            player_idle.idle_for_acceuil()
            screen.blit(player_idle.image, player_idle.rect)

            screen.blit(profile_image,(screen.get_width() - profile_image.get_width() - 250, 20))
            # Affichage du texte du nom d'utilisateur
            screen.blit(username_text,(screen.get_width() - profile_image.get_width() - 150, profile_image.get_height()//2 +15))
        if Credits:
            screen.blit(retour_image,rect_retour_image)
            y = start_y
            for line in lines:
                x = (screen.get_width() - line.get_width()) // 2
                screen.blit(line, (x, y))
                y += line.get_height() + 20

            start_y -= 5  # fait défiler vers le haut

            if y < 0:
                start_y = screen.get_height()  # recommencer le défilement
        pygame.display.update()

def charger_item_depuis_nom(conn, nom_item):
    cursor = conn.cursor()
    cursor.execute("SELECT name, stack_max, regen, type FROM Item WHERE name = ?", (nom_item,))
    row = cursor.fetchone()
    if row:
        name, stack_max, regen, type_ = row
        return Item(name, stack_max, regen, 0, 0, type_)
    return None 

def charger_inventaire(username):
    global font
    # Connexion à la base de données
    conn = sqlite3.connect('database/data_yahya.db')
    cursor = conn.cursor()
    # Requête pour récupérer les données de l'inventaire
    cursor.execute("SELECT slot_index, item_name, quantity FROM Inventaire WHERE pseudo = ?", (username,))
    donnees = cursor.fetchall()
    
    inventaire = [{}]*10  # 10 slots
    icones = [pygame.image.load(f"Items/slot.png")]*10 
    stack = [font.render("", True, (255, 255, 255))]*10

    for slot_index, nom_item, quantite in donnees:
        item = charger_item_depuis_nom(conn, nom_item)
        if item:
            print(slot_index)
            inventaire[slot_index] = {
                "name": nom_item,
                "object": item,
                "quantity": quantite,
                "icon": item.icon  
            }
            icones[slot_index] = item.icon
            stack[slot_index] = font.render(str(quantite), True, (255, 255, 255))
        else : 
            inventaire[slot_index] = {}
            icones[slot_index] = pygame.image.load(f"Items/slot.png")
            stack[slot_index] = font.render("", True, (255, 255, 255))
    return inventaire, icones, stack
# Fonction qui charge l'inventaire principal
def charger_inventaire_principal(username):
    global font
    conn = sqlite3.connect('database/data_yahya.db')
    cursor = conn.cursor()
    cursor.execute("SELECT row, col, item_name, quantity FROM InventairePrincipal WHERE pseudo = ?", (username,))
    donnees = cursor.fetchall()

    # Grille 6x5 : 6 colonnes, 5 lignes
    inventaire_principal = [[{} for _ in range(6)] for _ in range(5)]
    icones_principal = [[pygame.image.load("Items/slot.png") for _ in range(6)] for _ in range(5)]
    stack_principal = [[font.render("", True, (255, 255, 255)) for _ in range(6)] for _ in range(5)]

    for row, col, nom_item, quantite in donnees:
        item = charger_item_depuis_nom(conn, nom_item)
        if item:
            inventaire_principal[row][col] = {
                "name": nom_item,
                "object": item,
                "quantity": quantite,
                "icon": item.icon
            }
            icones_principal[row][col] = item.icon
            stack_principal[row][col] = font.render(str(quantite), True, (255, 255, 255))
    
    conn.close()
    print(stack_principal)
    return inventaire_principal, icones_principal, stack_principal

#fonction permettant de charger le stuff du joueur
def charger_stuff(username):
    global font
    # Connexion à la base de données
    conn = sqlite3.connect('database/data_yahya.db')
    cursor = conn.cursor()
    # Requête pour récupérer les données de l'inventaire
    cursor.execute("SELECT slot_index, item_name, quantity FROM Stuff WHERE pseudo = ?", (username,))
    donnees = cursor.fetchall()
    
    stuff = [{}]*4  # 4 slots
    stuff_icones = [pygame.image.load(f"Items/slot.png")]*4  
    stuff_stack = [font.render("", True, (255, 255, 255))]*4

    for slot_index, nom_item, quantite in donnees:
        item = charger_item_depuis_nom(conn, nom_item)
        if item:
            print(slot_index)
            stuff[slot_index] = {
                "name": nom_item,
                "object": item,
                "quantity": quantite,
                "icon": item.icon 
            }
            stuff_icones[slot_index] = item.icon
            
        else : 
            stuff[slot_index] = {}
            stuff_icones[slot_index] = pygame.image.load(f"Items/slot.png")
            
    return stuff, stuff_icones

def charger_quete():
    # Connexion à la base de données
    conn = sqlite3.connect('database/data_yahya.db')
    cursor = conn.cursor()
    # Requête pour récupérer la position du joueur
    cursor.execute('''SELECT current_quete FROM Login WHERE pseudo = ?;''', (username,))
    result = cursor.fetchone()
    if result:
        return graphe_quetes.nodes[result[0]]["quete"]
    return None

def charger_map():
    # Connexion à la base de données
    conn = sqlite3.connect('database/data_yahya.db')
    cursor = conn.cursor()
    # Requête pour récupérer la position du joueur
    cursor.execute('''SELECT current_map FROM Login WHERE pseudo = ?;''', (username,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return None
# Fonction pour lancer le jeu 
def launch_game():
    global tree_positions, graphe_quetes
    
    current_map = charger_map()
    mainClock = pygame.time.Clock()
    # Chargement de la carte Tiled
    tmx_data = load_pygame(f"maps/{current_map}.tmx")  


    collision_rects = []

    for obj in tmx_data.objects:
        if obj.name == "collision" or obj.type == "collision":
            rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            collision_rects.append(rect)

    #----------------sons -------------------------
    open_iventory_sfx = pygame.mixer.Sound("music/open_inventory.mp3")
    footstep_sound = pygame.mixer.Sound("music/run_sfx.mp3")
    footstep_sound.set_volume(0.3)  # Volume entre 0.0 et 1.0
    quest_sfx = pygame.mixer.Sound("music/quest.mp3")
    #----------------------------------------------
    # Connexion à la base de données
    conn = sqlite3.connect('database/data_yahya.db')
    cursor = conn.cursor()
    # Requête pour récupérer la position du joueur
    cursor.execute('''SELECT pos_x,pos_y,health,mana,endurance FROM Login WHERE pseudo = ?;''', (username,))
    result = cursor.fetchone()
    pos_x,pos_y,health,mana,endurance = result
    player = Player(pos_x,pos_y, screen)  # Positionner le joueur
    player.health_value = health
    player.mana_value = mana
    player.endurance_value = endurance

    #instanciation de l'objet save_game
    save_menu = Save_game_y(screen)

    # Instanciation de l'objet book
    book = Book(screen)
    
    #quete courante de base
    current_quete = graphe_quetes.nodes["Q1"]["quete"]

    #Création des gobelins
    gobelin1 = Enemy("gobelin_epee",1086,425,"enemy",screen,(100,100))

    gobelin2 = Enemy("gobelin_epee",1095,490,"enemy",screen,(100,100))

    gobelin3 = Enemy("gobelin_epee",350,400,"enemy",screen,(100,100))

    slime1 = Slime("slime1","enemy",600,100,"suiveur",screen)
    #pnj2 = PNJ("Wizard",200,500,"pnj",screen)


    chest1 = Coffre("chest1",962,1402,0)
    
    #Instanciations des portail 
    portail1 = Portals("portal1",1220,30.25)
    
    # Création des arbres et ajout au groupe
    trees = [Arbre("arbre", x, y) for x, y in tree_positions]

    #panneau quetes
    panneau_quest_img = pygame.image.load("UI/fond_quete_ui.png")
    panneau_quest_img = pygame.transform.scale(panneau_quest_img,(700,174))

    police_quetes = pygame.font.Font("UI/dialog_font.ttf", 20)
    police_quetes_mission = pygame.font.Font("UI/dialog_font.ttf", 15)


    panneau_visible = False
    panneau_y = -200  # Position de départ hors écran
    panneau_target_y = 50  # Position finale
    temps_affichage_panneau = 3  # en secondes
    temps_depart_panneau = 0
    quete_affichee = None  # Instance de Quete

    map_data = pyscroll.data.TiledMapData(tmx_data)

    # Créer un groupe de rendu pour pyscroll
    map_layer = pyscroll.orthographic.BufferedRenderer(map_data, screen.get_size())
    map_layer.zoom = 2.2  # Facteur de zoom (1 = taille normale, 2 = zoomé x2)

    # Créer un groupe de sprites avec caméra centrée
    group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

    # Ajoute les objets au groupe
    group.add(player, layer=5)

    #On ajoute ici le coffre
    group.add(chest1,layer = 2)

    
    
    #On ajoute ici les gobelins
    #group.add(pnj2, layer = 2)

    
    troncs = []
    for x, y in tree_positions:
        feuillage = Feuillage(x, y)
        tronc = Tronc(x, y)
        tronc.feuillage = feuillage  # ← On associe le feuillage au tronc
        feuillage.tronc = tronc # ← On associe le tronc au feuillage
        group.add(tronc, layer=2)
        group.add(feuillage, layer=7)
        troncs.append(tronc)  # ← On garde une liste de tous les troncs si besoin
    
    
    #paraetre pour cinematique de début 
    cinematique = True
    camera_y_offset = 300  # distance verticale à compenser
    camera_vitesse = 120  # pixels/sec

    #parametre fondu noir 
    fondu_actif = True
    fondu_opacite = 255  # Noir total
    vitesse_fondu = 150  # Pixels par seconde

    surface_fondu = pygame.Surface(screen.get_size())
    surface_fondu.fill((0, 0, 0))
    surface_fondu.set_alpha(fondu_opacite)
    #paraetre pour le panneau de quête à afficher
    file_quete_a_afficher = []
    affichage_etape = None
    
    print("lien a faire : ",not graphe_quetes["Q1"]["Q2"].get("choix", False))
    print("lien a faire 2: ", graphe_quetes["Q1"]["Q2"].get("choix", True))

    # Fonction pour terminer une quête
    def terminer_quete(id_quete):
        nonlocal panneau_visible, panneau_y, panneau_target_y
        nonlocal temps_depart_panneau, quete_affichee, affichage_etape, file_quete_a_afficher

        # Récupérer la quête
        quete = graphe_quetes.nodes[id_quete]["quete"]
        quete.terminee = True
        quete.active = False

        
        suivantes = []  # Liste pour stocker les quêtes suivantes à activer automatiquement
        for suivante in graphe_quetes.successors(id_quete):  # Parcourt tous les successeurs de la quête terminée
            if not graphe_quetes[id_quete][suivante].get("choix", False):  # Vérifie si le lien n'a pas l'attribut "choix" à True
                suivantes.append(suivante)  # Ajoute ce successeur à la liste des suivantes à activer
        
        #Si la quête ne possède pas des succeseurs n'ayant pas le flag "choix"
        if not suivantes:
            # Afficher au moins "quête accomplie" même sans suite directe
            panneau_visible = True
            panneau_y = -200
            panneau_target_y = 50
            temps_depart_panneau = pygame.time.get_ticks()
            affichage_etape = "accomplie"
            quete_affichee = None
            file_quete_a_afficher = []
            print("→ quete accomplie sans suite automatique")
            return
        # Préparer l’affichage "quête accomplie"
        panneau_visible = True
        panneau_y = -200
        panneau_target_y = 50
        temps_depart_panneau = pygame.time.get_ticks()
        affichage_etape = "accomplie"
        file_quete_a_afficher = [graphe_quetes.nodes[s]["quete"] for s in suivantes] #On récupère les quêtes suivantes à afficher

        print("→ file_quete_a_afficher :", [q.nom for q in file_quete_a_afficher]) 
        quest_sfx.play()  # On joue le son de nouvelle quête

    
    def afficher_panneau_nouvelle_quete(quete):
        nonlocal current_quete,panneau_visible, panneau_y, panneau_target_y
        nonlocal temps_depart_panneau, quete_affichee, affichage_etape

        print(" Panneau nouvelle quête :", quete.id)
        current_quete = quete
        panneau_visible = True
        panneau_y = -200
        panneau_target_y = 50
        temps_depart_panneau = pygame.time.get_ticks()
        quete_affichee = quete
        affichage_etape = "nouvelle_quete"

    
    pnj1 = PNJ("Wizard",184,1251,"pnj",screen,(50,50),pnj1_dialog,panneau_callback=afficher_panneau_nouvelle_quete)
    
    
    #On ajoute ici les PNJ
    #group.add(pnj1, layer=2)


    def afficher_panneau_slide(screen, quete, y):
        # Affiche le panneau à la position y
        screen.blit(panneau_quest_img, (screen.get_width() // 2 - panneau_quest_img.get_width() // 2, y))
        
        titre = police_quetes.render('Nouvelle quête principale', True, (255, 255,0))

        lines = quete.description.split('\n')  # ← ici
        for i, line in enumerate(lines):
            desc = police_quetes_mission.render(line, True, (0, 0, 0))
            screen.blit(desc, (screen.get_width() // 2 - panneau_quest_img.get_width() // 2 +120, y + 65 + i * 30))# ← 25 px entre chaque ligne
        

        
        
        screen.blit(titre, (screen.get_width() // 2 - titre.get_width() // 2, y + 20))
        

    def afficher_panneau_texte(screen, titre_texte, desc_texte, y):
        screen.blit(panneau_quest_img, (screen.get_width() // 2 - panneau_quest_img.get_width() // 2, y))
        
        titre = police_quetes.render(titre_texte, True, (255, 255, 0))
        desc = police_quetes_mission.render(desc_texte, True, (0, 0, 0))

        screen.blit(titre, (screen.get_width() // 2 - titre.get_width() // 2, y + 20))
        screen.blit(desc, (screen.get_width() // 2 - desc.get_width() // 2, y + 70))

    

    # Fonction quit
    def quit():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        

    # Fonction input pour gérer les entrées clavier
    def input():
        if player.is_attacking:
            return  # ← NE RIEN FAIRE SI ATTAQUE EN COURS
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
            if not player.is_moving:
                footstep_sound.play(-1)  # -1 = boucle
                player.is_moving = True
                
        else:
            if player.is_moving:
                footstep_sound.stop()
                player.is_moving = False
            # Animation idle quand le joueur ne bouge pas
            if player.last_direction == "down":
                player.idle_down()
            elif player.last_direction == "up":
                player.idle_up()
            elif player.last_direction == "right":
                player.idle_right()
            elif player.last_direction == "left":
                player.idle_left()

    #-------------fonctions d'accomplissement des quêtes--------------------------------------------------------
    def accomplissement_quete3():
        nonlocal current_quete
        quete3 = graphe_quetes.nodes["Q3"]["quete"]

        if quete3.active and not quete3.terminee:
            # Compter les "buche1" dans l'inventaire et la barre d'inventaire
            count_buche = 0
            # Inventaire principal
            for item in player.inventory_list:
                if item and getattr(item, 'name', '') == "buche1":
                    count_buche += slot['quantity']
            # Barre d'inventaire rapide
            for slot in player.inventory_bar_list:
                if slot and 'object' in slot and getattr(slot['object'], 'name', '') == "buche1":
                    count_buche += slot['quantity']
            
            if count_buche >= 10 :
                terminer_quete("Q3")
                pnj1.parole = ["Merci d'avoir ramassé les 10 bûches !", "Tu as prouvé ta valeur en rendant\n service à un viel homme comme moi.","Je t'en suis reconnaisant.", "Pour te remercier, voila quelque chose\n qui te sera utile pour ton aventure.","Adieu ..."]
                # Récupérer le successeur de Q3 (s'il existe)
                suivants = list(graphe_quetes.successors("Q3"))
                if suivants:
                    current_quete = graphe_quetes.nodes[suivants[0]]["quete"]
    def accomplissement_quete4():
        nonlocal current_quete
        quete3 = graphe_quetes.nodes["Q4"]["quete"]

        if quete3.active and not quete3.terminee:
            # Compter les "buche1" dans l'inventaire et la barre d'inventaire
            count_apple = 0
            # Inventaire principal
            for item in player.inventory_list:
                if item and getattr(item, 'name', '') == "apple":
                    count_apple += slot['quantity']
            # Barre d'inventaire rapide
            for slot in player.inventory_bar_list:
                if slot and 'object' in slot and getattr(slot['object'], 'name', '') == "apple":
                    count_apple += slot['quantity']
            
            if count_apple == 5 :
                terminer_quete("Q4")
                pnj1.parole = ["Merci d'avoir ramassé les 5 pommes !", "Tu as prouvé ta valeur en rendant\n service à un viel homme comme moi.","Je t'en suis reconnaisant.", "Pour te remercier, voila quelque chose\n qui te sera utile pour ton aventure.","Adieu ..."]
                # Récupérer le successeur de Q3 (s'il existe)
                suivants = list(graphe_quetes.successors("Q3"))
                if suivants:
                    current_quete = graphe_quetes.nodes[suivants[0]]["quete"]
    
    #-----------------------------------------------------------------------------------------------------------
    
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




    

    running = True
    near_chest = None  # coffre à proximité par défaut à None


    Show_stats = False

    active_pnj = None
    can_attack = True

    fps_font = pygame.font.SysFont("arial", 20)
    
    
        
    
    while running:
        dt = mainClock.tick(60) / 1000  # Temps écoulé en secondes

        #Lancement de la cinématique
        if cinematique:
            moving = False
            # Centre sur une position décalée progressivement vers le joueur
            current_offset = max(0, camera_y_offset - camera_vitesse * dt)
            camera_y_offset = current_offset

            camera_target = (player.rect.centerx, player.rect.centery - int(current_offset))
            group.center(camera_target)

            if camera_y_offset <= 0:
                cinematique = False  # Fin de l'animation
                # Lancer l'affichage de la quête d'intro au début du jeu
                quete_affichee = charger_quete() #On charge la quête enregistrer dans la base de donnée à l'aide de la fonction charger_quete()
                
                # On charge ici la barre d'inventaire du joueur
                player.inventory_bar_list,player.inventory_icons,player.stack_text = charger_inventaire(username)
                # On charge ici l'inventaire du joueur
                player.inventory_list,player.inventory_bag_icon,inventory_bag_stack_text = charger_inventaire_principal(username)
                # On charge ici le stuff du joueur
                player.armour_list,player.armour_icon_list = charger_stuff(username)
                
                
                quete_affichee.active = True
                current_quete = graphe_quetes.nodes[quete_affichee.id]["quete"] #on stocke ici la quête en cours
                pnj1.restaurer_etat_quete() #On restaure la quete qui a été faite afin de ne pas retomber sur le dialogue de proposition du pnj enn cas d'interaction avec lui
                panneau_visible = True
                panneau_y = -200
                panneau_target_y = 50
                temps_depart_panneau = pygame.time.get_ticks()
                affichage_etape = "nouvelle_quete"
        else:
            group.center(player.rect.center)
            moving = True
        for event in pygame.event.get():
            quit()
            if event.type == pygame.KEYDOWN:
                #Gestion desévenement de la touche [i]
                if event.key == pygame.K_e:
                    open_iventory_sfx.play()  # On joue le son d'ouverture de l'inventaire
                    show_inventory = not show_inventory  # On inverse l'état de l'inventaire
                    player.OnBag = True
                    player.OnArmour = False
                    moving = not moving
                elif event.key == pygame.K_F3:
                    Show_stats = not Show_stats
                    
            
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if show_inventory == False and player.dead == False and can_attack:
                    player.handle_mouse_attack(group)

                if player.rect_button_armour.collidepoint(event.pos):
                    player.OnArmour = True
                    player.OnBag = False
                if player.rect_button_bag.collidepoint(event.pos):
                    player.OnArmour = False
                    player.OnBag = True
                
                book.handle_mouse_event(event)

                if player.dead:
                    #On gère ici l'appuie sur les boutton du menu de mort
                    if player.rect_reesayer_dead.collidepoint(event.pos):
                        player = Player(pos_x, pos_y, screen)
                        group.add(player, layer=5)
                        
                    if player.rect_quiiter_dead.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                        

            if show_inventory and player.dead == False:
                player.handle_mouse_events(event)

            player.handle_key_events(event)

            save_menu.handle_event(event,username,player.level,player.rect.x,player.rect.y,player.health_value,player.mana_value,player.endurance_value,current_quete.id,player.inventory_bar_list,player.inventory_list,player.armour_list,current_map)

            if event.type == pygame.KEYDOWN:
                #Gestion desévenement de la touche [i]
                if event.key == pygame.K_i:
                    if near_chest and near_chest.Can_open:
                        near_chest.start_animation_coffre(near_chest.coffre_open_list, 0.3)
                        # Si la quête actuelle est "Q1", on la termine
                        quete = graphe_quetes.nodes["Q1"]["quete"]
                        print("état de la quêtes", quete.active, quete.terminee)
                        if quete.active and not quete.terminee:
                            terminer_quete("Q1")
                            current_quete = graphe_quetes.nodes["Q2"]["quete"]

                    elif active_pnj:  # ← Si on a un PNJ actif
                        active_pnj.CanDialog = not active_pnj.CanDialog
                        if active_pnj.CanDialog:

                            active_pnj.start_dialog(0)
                            # Gérer la fin de la quête précédente (Q2)
                            q2 = graphe_quetes.nodes["Q2"]["quete"]
                            if q2.active and not q2.terminee:
                                terminer_quete("Q2")
      
                #Gestion desévenement de la touche [ESPACE]
                if event.key == pygame.K_SPACE:
                    if active_pnj and active_pnj.CanDialog:
                        active_pnj.next_dialog()
                        q5 = graphe_quetes.nodes["Q5"]["quete"]

                        if q5.active and not q5.terminee : 
                            # On termine la quête 5 uniquement si on est à la dernière phrase du dialogue
                            if active_pnj.current_parole_index >= len(active_pnj.parole)-1:
                                terminer_quete("Q5")
                                # Récupérer le successeur de Q5 (s'il existe)
                                suivants = list(graphe_quetes.successors("Q5"))
                                if suivants:
                                    current_quete = graphe_quetes.nodes[suivants[0]]["quete"]
                
        

        # Ajout dynamique du PNJ1 si la quête Q2, Q3, Q4 ou Q5 est active ou terminée
        if not any(isinstance(s, PNJ) and getattr(s, "name", "") == "Wizard" for s in group.sprites()):
            quetes_pnj = ["Q2", "Q3", "Q4", "Q5","Q6"]
            for q in quetes_pnj:
                quete = graphe_quetes.nodes[q]["quete"]
                if quete.active or quete.terminee:
                    group.add(pnj1, layer=2)
                    break
        
        quetes_por = ["Q6"]
        for q in quetes_por:
            quete = graphe_quetes.nodes[q]["quete"]
            if quete.active or quete.terminee:
                group.add(portail1,layer = 4)
                group.add(gobelin1,layer = 3)
                group.add(gobelin2,layer = 3)
                break


  
                   

        
        # vérifier si l'on peut marcher
        if not cinematique and player.dead == False:
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

        # Si la quête 5 est active et la précédente était la quête 3, on change le dialogue du PNJ
        if graphe_quetes.nodes["Q5"]["quete"].active:
            pred = list(graphe_quetes.predecessors("Q5"))
            if pred:
                if pred[0] == "Q3":
                    pnj1.parole = pnj1_dialog_apres_Q3 #On charge le dialogue du pnj depuis dialog_data pour alléger le code

                elif pred[0] == "Q4":
                    pnj1.parole = pnj1_dialog_apres_Q4 #On charge le dialogue du pnj depuis dialog_data pour alléger le code
        if graphe_quetes.nodes["Q6"]["quete"].active:
            pnj1.parole = ["Bon voyage aventurier..."]
                

                    

        group.update(dt)
        
        
        
        group.draw(screen)
        

        if book.OnBook:
            book.animBook()

        if progressing:
            world_pos = (player.rect.centerx , player.rect.top - 20)
            screen_pos = map_layer.translate_point(world_pos)

            radius = 30
            end_angle = -math.pi / 2 + progress * 2 * math.pi
            pygame.draw.circle(screen, (100, 100, 100), screen_pos, radius, 3)
            pygame.draw.arc(screen, (0, 200, 0), (screen_pos[0] - radius, screen_pos[1] - radius, radius * 2, radius * 2),
                            -math.pi / 2, end_angle, 4)

            screen.blit(eat_image, (screen_pos[0] - 30, screen_pos[1] - 27))
        
        #régéneration des point d'attaques
        if player.remaining_attacks < player.max_attacks:
            player.attack_regen_timer += dt * 1000  # dt est en secondes → ms
            if player.attack_regen_timer >= player.attack_regen_delay:
                player.remaining_attacks += 1
                player.attack_regen_timer = 0

        #changement de la vitesse de coupe de l'arbre si l'on a une hache    
        if player.inventory_bar_list[player.inventory_index] != {}:
            if player.inventory_bar_list[player.inventory_index]['object'].type == "Hache":
                fill_time_cut = 4
            else:
                fill_time_cut = 8
        near_chest = None  # Reset à chaque frame
        

        

        for sprite in group.sprites():

            if isinstance(sprite, Portals) and player.feet.colliderect(sprite.rect):
                if sprite.name == "portal1":
                    # Afficher un écran noir avec "Téléportation"
                    screen.fill((0, 0, 0))
                    font_teleport = pygame.font.Font("UI/dialog_font.ttf", 60)
                    text_teleport = font_teleport.render("Téléportation...", True, (255, 255, 255))
                    text_rect = text_teleport.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
                    screen.blit(text_teleport, text_rect)
                    pygame.display.flip()
                    pygame.time.delay(900)
                    # Téléportation vers la nouvelle map "map_principale1"
                    # Charger la nouvelle map
                    tmx_data_new = load_pygame("maps/map_principale1.tmx")
                    map_data_new = pyscroll.data.TiledMapData(tmx_data_new)
                    map_layer_new = pyscroll.orthographic.BufferedRenderer(map_data_new, screen.get_size())
                    map_layer_new.zoom = 2.2

                    # Trouver la position de départ du joueur sur la nouvelle map
                    try:
                        player_start = tmx_data_new.get_object_by_name("Player")
                        player.rect.x = player_start.x
                        player.rect.y = player_start.y
                    # Sinon on le met par défaut en (0,0)
                    except Exception:
                        player.rect.x = 0
                        player.rect.y = 0

                    # Mettre à jour le groupe de rendu avec la nouvelle map
                    group._map_layer = map_layer_new
                    group.center(player.rect.center)
                    # Mettre à jour les collisions pour la nouvelle map
                    collision_rects.clear()
                    for obj in tmx_data_new.objects:
                        if obj.name == "collision" or obj.type == "collision":
                            rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                            collision_rects.append(rect)
                    current_map = "map_principale1"
                    # Optionnel : retirer/ajouter les entités spécifiques à la nouvelle map ici
                    # Retirer toutes les entités de la map précédente (hors joueur)
                    for sprite in group.sprites():
                        if sprite != player:
                            group.remove(sprite)
                    q6 =  graphe_quetes.nodes["Q6"]["quete"]
                    if q6.active or not q6.terminee:
                        terminer_quete("Q6")
                        current_quete = graphe_quetes.nodes["Q7"]["quete"]
                    

                    continue  # pour éviter d'autres collisions ce frame

            if show_inventory == False:
                if isinstance(sprite, Tronc) and player.hit_box.colliderect(sprite.hitbox):
                    
                    if sprite.Can_cut:
                        if pygame.mouse.get_pressed()[0]:
                            if not cut_progressing:
                                player.is_attacking = False
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
                                    group.add(Item("buche1", 24, 10, sprite.rect.x + 50, sprite.rect.y + 50, "Wood"))
                                    group.add(Item("buche1", 24, 10, sprite.rect.x + 30, sprite.rect.y + 30, "Wood"))
                                    group.add(Item("buche1", 24, 10, sprite.rect.x + 20, sprite.rect.y + 50, "Wood"))
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
                            world_pos = (player.rect.centerx, player.rect.top - 30)
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
            
            if isinstance(sprite, Feuillage) and player.hit_box.colliderect(sprite.hitbox):
                sprite.image.set_alpha(100)  # Rendre le feuillage transparent
                if sprite.tronc.Can_cut:
                    sprite.tronc.image.set_alpha(100)
                else:
                    sprite.tronc.image.set_alpha(255)
                

            elif isinstance(sprite, Feuillage):
                sprite.image.set_alpha(255)  # Restaurer l'opacité si le joueur ne collisionne plus
                sprite.tronc.image.set_alpha(255)
        #On gere ici les collision aves les objets de type "Coffre"
            if isinstance(sprite, Coffre) and player.feet.colliderect(sprite.rect):
                
                player.move_back()

            if isinstance(sprite, Coffre) and player.hit_box.colliderect(sprite.rect):
                near_chest = sprite  # On garde en mémoire le coffre à proximité
                if sprite.Can_open:
                    world_pos = (player.rect.centerx , player.rect.top - 10)
                    screen_pos = map_layer.translate_point(world_pos) #On récupère la poistion relative à la map
                    screen.blit(player.key_board_I, (screen_pos[0]-23, screen_pos[1]+30))#affichage de la touche I quand on est à proximité d'un coffre

            if isinstance(sprite, Item) and player.hit_box.colliderect(sprite.rect) and sprite.en_animation_sortie == False:
                group.remove(sprite)  # Supprime l'objet du groupe
                player.add_to_inventory(sprite)

            if isinstance(sprite, Entity) and player.feet.colliderect(sprite.hit_box):
                player.move_back()

            if isinstance(sprite, PNJ):
                if player.hit_box.colliderect(sprite.champ_vision):
                    
                    active_pnj = sprite  # ← Le PNJ actif devient celui détecté
                    world_pos = (player.rect.centerx , player.rect.top - 10)
                    screen_pos = map_layer.translate_point(world_pos)
                    screen.blit(player.key_board_I, (screen_pos[0]-23, screen_pos[1]+30))
                else:
                    if active_pnj == sprite:
                        sprite.CanDialog = False   # On FERME la boîte de dialogue
                        active_pnj = None

            if isinstance(sprite, Enemy):

                sprite.champ_vision_enemy.center = sprite.rect.center  # Toujours mettre à jour le champ de vision
                sprite.follow_player(player,[gobelin1,gobelin2,gobelin3])
                if sprite.distance_between_player_enemy <=20:
                    sprite.animation(sprite.right_attack,0.12,(100,100))
                # Si knockback est actif
                if sprite.knockback:
                    sprite.rect.x += sprite.knockback_direction * sprite.knockback_speed
                    sprite.knockback_speed -= 0.5  # on ralentit progressivement
                    if sprite.knockback_speed <= 0:
                        sprite.knockback = False
                        sprite.knockback_speed = 0

                sprite.draw_health_bar(screen,map_layer)
            if isinstance(sprite, Enemy) and player.hit_box.colliderect(sprite.rect) :
                if player.health_value < 0:
                    player.health_value = 0
                if player.health_value == 0:
                    player.dead = True
                    group.remove(player)

            if isinstance(sprite,Slime):
                sprite.champ_vision_enemy.center = sprite.rect.center  # Toujours mettre à jour le champ de vision
                
                if sprite.category == "suiveur":
                    sprite.follow_player(player,[slime1])
                    
                    
                if sprite.category == "kamikaze":
                    
                    sprite.follow_player_optional(player)
                    
                    if sprite.distance_between_player_slime <= 10 and sprite.category == "kamikaze":
                        sprite.kamikaze(sprite,group,player)
                    
                    
                
                sprite.draw_health_bar(screen,map_layer)

            

        # On gère ici le recul du personnage
        if player.knockback:
            player.rect.x += player.knockback_direction * player.knockback_speed
            player.hit_box.x += player.knockback_direction * player.knockback_speed
            player.rect.y += player.knockback_direction_y * player.knockback_speed
            
            player.knockback_speed -= 0.5  # on ralentit progressivement
            if player.knockback_speed <= 0:
                player.knockback = False
                player.knockback_speed = 0     


                
                

        # Collision avec la map (rectangles Tiled)
        for rect in collision_rects:
            if player.feet.colliderect(rect):
                player.move_back()
                

        #On reférifie si la vie est en dessous de 0 
        if player.health_value < 0:
            player.health_value = 0 # Si c'est le cas on remet la vie à zéro

        #On reférifie si le mana est en dessous de 0 
        if player.mana_value < 0:
            player.mana_value = 0 # Si c'est le cas on remet la vie à zéro

        #On vérifie si la vie est à zéro
        if player.health_value == 0:
            player.dead = True # Si c'est le cas on met player.dead à zéro 
            group.remove(player) # on remove le joueur du group


        #-----gestion de l'accomplissement des quêtes sans avoir besoin de rencontrer une entité----

            
        accomplissement_quete3()
        accomplissement_quete4()
        #-------------------------------------------------------------------------------------------

        #affichage des UI 
        player.affiche_ui(map_layer)
        book.affiche_book_ui()
        
       
        
        if show_inventory:
            player.display_inventory()  # On appelle la méthode display_inventory pour afficher l'inventaire

        if save_menu.quitte :
            moving = False
            can_attack = False
        else: 
            moving = True
            can_attack = True
        
      
       


        pnj1.updatee(dt)
        
        save_menu.update()
        chest1.anim_chest(group,near_chest)
        
        
        pnj1.idle()
        portail1.anim_portal()
 
        #gestion de l'affichage des panneau des quête
        if panneau_visible:
            

            if panneau_y < panneau_target_y:
                panneau_y += 10
                if panneau_y > panneau_target_y:
                    panneau_y = panneau_target_y

            # Étape : Quête accomplie
            if affichage_etape == "accomplie":
                afficher_panneau_texte(screen, "Quête accomplie !", "Nouvelle quête débloquée.", panneau_y)
                
                if (pygame.time.get_ticks() - temps_depart_panneau) / 1000 > temps_affichage_panneau:
                    if file_quete_a_afficher:
                        panneau_y = -200
                        temps_depart_panneau = pygame.time.get_ticks()
                        quete_affichee = file_quete_a_afficher.pop(0)
                        quete_affichee.active = True
                        affichage_etape = "nouvelle_quete"
                    else:
                        panneau_visible = False
                        affichage_etape = None
                        quete_affichee = None
                        panneau_y = -200

            elif affichage_etape == "nouvelle_quete":
                if quete_affichee:
                    afficher_panneau_slide(screen, quete_affichee, panneau_y)
                
                if (pygame.time.get_ticks() - temps_depart_panneau) / 1000 > temps_affichage_panneau:
                    if file_quete_a_afficher:
                        panneau_y = -200
                        temps_depart_panneau = pygame.time.get_ticks()
                        quete_affichee = file_quete_a_afficher.pop(0)
                        quete_affichee.active = True
                    else:
                        panneau_visible = False
                        affichage_etape = None
                        quete_affichee = None
                        panneau_y = -200

            


        #affichage des stats génerale du jeu : (FPS, pos_x,pox_y)
        if Show_stats:
            fps = int(mainClock.get_fps())
            fps_text = fps_font.render(f"FPS : {fps}", True, (255, 255, 0))
            x_position = fps_font.render(f"X : {player.rect.x}", True, (255, 255, 0))
            y_position = fps_font.render(f"Y : {player.rect.y}", True, (255, 255, 0))
            screen.blit(fps_text, (800, 10))
            screen.blit(x_position,(900,10))
            screen.blit(y_position,(900,50))
        #gestion du fondu lors du début du jeu 
        if fondu_opacite <= 0 and camera_y_offset <= 0:
            cinematique = False
            fondu_actif = False
            moving = True
        #lorsqu'on quitte le jeu on passe sur le menu principal
        if save_menu.running == False:
            main_menu()
        # ---- Fondu noir de début ----
        if fondu_actif:
            fondu_opacite = max(0, fondu_opacite - vitesse_fondu * dt)
            surface_fondu.set_alpha(int(fondu_opacite))
            screen.blit(surface_fondu, (0, 0))

            if fondu_opacite <= 0:
                fondu_actif = False
        


        # On remplit la liste des quêtes proposées par le PNJ avec les successeurs de Q2 ayant choix=True, si la quête actuelle est Q2
        pnj1.choix_de_quetes = [graphe_quetes.nodes[s]["quete"] for s in graphe_quetes.successors("Q2") if graphe_quetes["Q2"][s].get("choix", False)
        ] if current_quete.id == "Q2" else []

        pygame.display.update()

if __name__ == "__main__":
    login()
    pygame.event.clear()
    main_menu()
    pygame.event.clear()
