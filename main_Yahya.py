
import random
from quete_secondaire import *
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

from pygame.locals import *
import pyscroll
import pyscroll.data
import time
from objects_Yahya import *
from random import *
pygame.init()
pygame.key.set_repeat(400, 20)  # délai initial 400ms, puis 40ms entre répétitions
pygame.display.set_caption("Jeu")
from scripte.save_game import*
from classe_enemy_Yahya import *
from scripte.pnj import *
import pygame
from classe_entity_Yahya import *
from dialog_data import *

from login_class import *
import networkx as nx



# Création du graphe dirigé
graphe_quetes = nx.DiGraph()

# Création des objets quête
q1 = Quete("Q1", "Trouver le coffre", "Suivez le chemin et trouvez le coffre.")
q2 = Quete("Q2", "Trouver le guide", "Trouver le guide dans le bois.")

q3 = Quete("Q3", "Ramasser du bois", "Ramasser 10 buches dans la forêt.")
q4 = Quete("Q4","Récupérer des pommes","Ramasser 5 pommes dans la foret")


# Ajout des nœuds avec attributs
graphe_quetes.add_node("Q1", quete=q1)
graphe_quetes.add_node("Q2", quete=q2)
graphe_quetes.add_node("Q3", quete=q3)
graphe_quetes.add_node("Q4",quete = q4)
# Ajout des relations (choix ou dépendances)
graphe_quetes.add_edge("Q1", "Q2")  # Après Q1, Q2 est possible
graphe_quetes.add_edge("Q2", "Q3",choix=True)  # Après Q2, Q3 est possible
graphe_quetes.add_edge("Q2","Q4",choix=True)     # Après Q2, Q4 est possible



username = ""
def on_login():
    print("hey")
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
    conn = sqlite3.connect('database/data.db')
    cursor = conn.cursor()

    # Requête pour vérifier si le nom d'utilisateur et le mot de passe existent dans la table "users"
    cursor.execute('''SELECT pseudo,password FROM Login WHERE pseudo=? AND password=?;''', (username, password))
    result = cursor.fetchall()

    # Fermer la connexion à la base de données
    conn.close()

    if result is not None:
        return True  # Identifiant et mot de passe valides
    

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
    
    tmx_data = load_pygame("maps/maps.tmx")  
    player_position = tmx_data.get_object_by_name("Player")
    if password == confirm_password:
        # Connexion à la base de données SQLite
        conn = sqlite3.connect('database/data.db')
        cursor = conn.cursor()

        # Requête pour vérifier si le nom d'utilisateur existe déjà dans la table "users"
        cursor.execute('''INSERT INTO Login (pseudo,password,pos_x,pos_y,health,mana,endurance,level) values (?,?,?,?,100,0,100,0) ''',(username,password,player_position.x,player_position.y))
        cursor.close()
        conn.commit()
        conn.close()
        return True
    else :
        font = pygame.font.Font("UI/dialog_font.ttf", 15)
        message_erreur = font.render("Les mots de passe ne correspondent pas", True, (255, 0, 0))
        screen.blit(message_erreur, (x_pannel_create_an_account ,y_pannel_create_an_account))

    

def login():

    global username

    Login = True
    Confirm = False
    background_image = pygame.image.load("UI/bg_menu.png")
    background_image = pygame.transform.scale(background_image, screen.get_size())
    logo_image = pygame.image.load("UI/Logo.png")

    pannel_create_an_account = pygame.image.load("UI/create_account.png")
    x_pannel_create_an_account = screen.get_width() // 2 - pannel_create_an_account.get_width() // 2
    y_pannel_create_an_account = screen.get_height()//2 - pannel_create_an_account.get_height()//2
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
    message_erreur = font.render("Identifiant/Mot de passe invalide", True, (255, 0, 0))

    # rectangle de création de compte
    btn_create_account = pygame.Rect(x_pannel_create_an_account + 153, y_pannel_create_an_account + 363, 181, 52)
    
    if Login:
        logo_image = pygame.transform.scale(logo_image, (600, 600))
        
        

        rect = pygame.Rect(x + 122, y + 247, 181, 52)
        
        pannel = pygame.image.load("UI/loginv2.png.png")
        rect_pannel = pannel.get_rect()
        rect_pannel.x = x
        rect_pannel.y = y
        
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
                        if verification(username_box.text,password_box.text):
                            running = False
                            username = username_box.text
                            print("Login successful")
                            return
                        else : screen.blit(message_erreur, (x_pannel_create_an_account ,y_pannel_create_an_account))
                        
                    if rect_creer_compte.collidepoint(event.pos):
                        Login = False
                        Confirm = True
                        
                    if rect_oeil_ouvert1.collidepoint(event.pos):
                        if Can_see_password == False:
                            password_box.set_password_mode(False)  # ou False
                            Can_see_password = True
                            oeil_ouvert1 = oeil_ferme
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
                        else:
                            confirm_password_box1.set_password_mode(True)
                            Can_see_password = False
                            oeil_ouvert3 = pygame.image.load("UI/oeil_ouvert.png")
                            oeil_ouvert3 = pygame.transform.scale(oeil_ouvert1,(50,50))
                    if rect_retour_image.collidepoint(event.pos):
                        Login = True
                        Confirm = False
                    if btn_create_account.collidepoint(event.pos):
                        if create_account(username_box1.text,password_box1.text,confirm_password_box1.text):
                            running = False
                            username = username_box1.text
                            print("Login successful")
                        else : screen.blit(message_erreur, (x_pannel_create_an_account ,y_pannel_create_an_account))
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
            screen.blit(message_erreur, (x_pannel_create_an_account ,y_pannel_create_an_account))
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
    while running_menu:
        mouse_pos = pygame.mouse.get_pos()
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    return
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        screen.blit(background_image, (0, 0))

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
        pygame.display.update()

# Fonction pour lancer le jeu 
def launch_game():
    global tree_positions, graphe_quetes
    

    mainClock = pygame.time.Clock()
    # Chargement de la carte Tiled
    tmx_data = load_pygame("maps/maps.tmx")  


    collision_rects = []

    for obj in tmx_data.objects:
        if obj.name == "collision" or obj.type == "collision":
            rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            collision_rects.append(rect)


    player_position = tmx_data.get_object_by_name("Player")
    x_tmp = player_position.x
    y_tmp = player_position.y
    player = Player(x_tmp, y_tmp, screen)  # Positionner le joueur

    save_menu = Save_game(screen)
    chest_position = tmx_data.get_object_by_name("coffre1")

    

    #Création des gobelins
    gobelin1 = Enemy("gobelin_epee",250,300,"enemy",screen,(100,100))

    gobelin2 = Enemy("gobelin_epee",350,250,"enemy",screen,(100,100))

    gobelin3 = Enemy("gobelin_epee",350,400,"enemy",screen,(100,100))

    slime1 = Slime("slime1","enemy",600,100,"suiveur",screen)
    #pnj2 = PNJ("Wizard",200,500,"pnj",screen)
    chest1 = Coffre("chest1",chest_position.x,chest_position.y)

    item = Item("pain", 24, 30, 352, 350, "Food")
    item2 = Item("plastron", 1, 10, 300, 450, "Plastron")
    item3 = Item("casque", 1, 10, 500, 270, "Casque")





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
    temps_affichage_panneau = 5  # en secondes
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
    group.add(item)
    group.add(item2)
    group.add(item3)


    #On ajoute ici le coffre
    group.add(chest1,layer = 2)

    

    #On ajoute ici les gobelins
    group.add(gobelin1,layer = 4)
    group.add(gobelin2,layer = 4)
    group.add(gobelin3, layer = 4)
    #group.add(pnj2, layer = 2)

    group.add(slime1 ,layer = 4)
    troncs = []
    for x, y in tree_positions:
        feuillage = Feuillage(x, y)
        tronc = Tronc(x, y)
        tronc.feuillage = feuillage  # ← On associe le feuillage au tronc
        feuillage.tronc = tronc # ← On associe le tronc au feuillage
        group.add(tronc, layer=2)
        group.add(feuillage, layer=7)
        troncs.append(tronc)  # ← On garde une liste de tous les troncs si besoin
    
    file_quete_a_afficher = []
    affichage_etape = None

    # Fonction pour terminer une quête
    def terminer_quete(id_quete):
        nonlocal panneau_visible, panneau_y, panneau_target_y
        nonlocal temps_depart_panneau, quete_affichee, affichage_etape, file_quete_a_afficher

        print("→ terminer_quete appelée pour :", id_quete)

        # Récupérer la quête
        quete = graphe_quetes.nodes[id_quete]["quete"]
        quete.terminee = True
        quete.active = False

        # Successeurs SANS le flag "choix" (donc à activer automatiquement)
        suivantes = [
            s for s in graphe_quetes.successors(id_quete)
            if not graphe_quetes[id_quete][s].get("choix", False)
        ]

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
        file_quete_a_afficher = [graphe_quetes.nodes[s]["quete"] for s in suivantes]

        print("→ file_quete_a_afficher :", [q.id for q in file_quete_a_afficher])


    
    def afficher_panneau_nouvelle_quete(quete):
        nonlocal panneau_visible, panneau_y, panneau_target_y
        nonlocal temps_depart_panneau, quete_affichee, affichage_etape

        print(" Panneau nouvelle quête :", quete.id)
        panneau_visible = True
        panneau_y = -200
        panneau_target_y = 50
        temps_depart_panneau = pygame.time.get_ticks()
        quete_affichee = quete
        affichage_etape = "nouvelle_quete"

    pnj1 = PNJ("Wizard",200,200,"pnj",screen,(50,50),pnj1_dialog,panneau_callback=afficher_panneau_nouvelle_quete)
    #On ajoute ici les PNJ
    group.add(pnj1, layer=2)


    def afficher_panneau_slide(screen, quete, y):
        # Affiche le panneau à la position y
        screen.blit(panneau_quest_img, (screen.get_width() // 2 - panneau_quest_img.get_width() // 2, y))
        
        titre = police_quetes.render('Nouvelle quête principale', True, (255, 255,0))
        desc = police_quetes_mission.render(quete.description, True, (0, 0, 0))
        
        screen.blit(titre, (screen.get_width() // 2 - titre.get_width() // 2, y + 20))
        screen.blit(desc, (screen.get_width() // 2 - panneau_quest_img.get_width() // 2 +120, y + 65))

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


    Show_stats = False
    can_talk_to_pnj1 = False

    active_pnj = None
    can_attack = True
    bois_recolte = 0
    fps_font = pygame.font.SysFont("arial", 20)

    # Lancer l'affichage de la quête d'intro au début du jeu
    quete_affichee = graphe_quetes.nodes["Q1"]["quete"]
    quete_affichee.active = True
    panneau_visible = True
    panneau_y = -200
    panneau_target_y = 50
    temps_depart_panneau = pygame.time.get_ticks()
    affichage_etape = "nouvelle_quete"
    
    
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
                elif event.key == pygame.K_F3:
                    Show_stats = not Show_stats
                    
            
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if show_inventory == False and player.dead == False and can_attack:
                    # Animation attaque
                    if player.last_direction == "right":
                        player.start_anim_attack(player.attack_right_mouv, 0.3, 0)
                            #Le joueur peut attaquer
                        player.is_attacking = True
                        
                    if player.last_direction == "left":
                        player.start_anim_attack(player.attack_left_mouv, 0.3, -0)

                        #Le joueur peut attaquer
                        player.is_attacking = True

                    # Définir une direction de dash
                    direction = pygame.math.Vector2(0, 0)
                    if player.last_direction == "right":
                        direction = pygame.math.Vector2(1, 0)
                    elif player.last_direction == "left":
                        direction = pygame.math.Vector2(-1, 0)

                    # Lancer le dash
                    player.dash_vector = direction * player.dash_speed
                    player.dashing = True
                    player.dash_timer = player.dash_duration

                    # Vérifie l'attaque sur les ennemis
                    for sprite in group.sprites():
                        if isinstance(sprite, Enemy) or isinstance(sprite, Slime):
                            if player.last_direction == "right" :
                                if player.attack_box_right.colliderect(sprite.rect):
                                    sprite.current_health -= player.degats  # Inflige 10 points de dégâts
                                    
                                    if sprite.current_health < 0:
                                        sprite.current_health = 0
                                    if sprite.current_health == 0:
                                        sprite.dead(group,sprite)
                                    sprite.knockback = True
                                    sprite.knockback_speed = 6
                                    sprite.knockback_direction = 1

                            if player.last_direction == "left" :
                                if player.attack_box_left.colliderect(sprite.rect):
                                    sprite.current_health -= player.degats  # Inflige 10 points de dégâts

                                    if sprite.current_health < 0:
                                        sprite.current_health = 0
                                    if sprite.current_health == 0:
                                        sprite.dead(group,sprite)

                                    sprite.knockback = True
                                    sprite.knockback_speed = 6
                                    sprite.knockback_direction = -1

    
                                    


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

                if player.dead:
                    #On gère ici l'appuie sur les boutton du menu de mort
                    if player.rect_reesayer_dead.collidepoint(event.pos):
                        player = Player(player_position.x, player_position.y, screen)
                        group.add(player, layer=5)
                        
                    if player.rect_quiiter_dead.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                        

            if show_inventory and player.dead == False:
                player.handle_mouse_events(event)

            player.handle_key_events(event)

            save_menu.handle_event(event,"ruen",1,player.rect.x,player.rect.y)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    if near_chest and near_chest.Can_open:
                        near_chest.start_animation_coffre(near_chest.coffre_open_list, 0.3)
                        # Si la quête actuelle est "Q1", on la termine
                        quete = graphe_quetes.nodes["Q1"]["quete"]
                        print("état de la quêtes", quete.active, quete.terminee)
                        if quete.active and not quete.terminee:
                            terminer_quete("Q1")
                            print(affichage_etape)
                            
                        
                    elif active_pnj:  # ← Si on a un PNJ actif
                        active_pnj.CanDialog = not active_pnj.CanDialog
                        if active_pnj.CanDialog:
                            active_pnj.start_dialog(0)
                            q2 = graphe_quetes.nodes["Q2"]["quete"]
                            if q2.active and not q2.terminee:
                                terminer_quete("Q2")
                                
                                # Récupérer manuellement les choix (Q3 et Q4)
                                q3 = graphe_quetes.nodes["Q3"]["quete"]
                                q4 = graphe_quetes.nodes["Q4"]["quete"]
                                active_pnj.proposer_quetes([q3, q4])

                if event.key == pygame.K_SPACE:
                    if active_pnj and active_pnj.CanDialog:
                        active_pnj.next_dialog()





        quete = graphe_quetes.nodes["Q2"]["quete"]
                      

        
        # vérifier si l'on peut marcher
        if moving and player.dead == False:
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

        


        group.update(dt)
        group.center(player.rect.center)  # Centre la caméra sur le joueur
        
        group.draw(screen)
        

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
                    screen_pos = map_layer.translate_point(world_pos)
                    screen.blit(player.key_board_I, (screen_pos[0]-23, screen_pos[1]+10))

            if isinstance(sprite, Item) and player.hit_box.colliderect(sprite.rect) and sprite.en_animation_sortie == False:
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

            

        # Si knockback est actif
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
                    

        player.affiche_ui()
        
        if show_inventory:
            player.display_inventory()  # On appelle la méthode display_inventory pour afficher l'inventaire

        if save_menu.quitte :
            moving = False
            can_attack = False
        else: 
            moving = True
            can_attack = True
        
      
       


        pnj1.update(dt)
        
        save_menu.update()
        chest1.anim_chest(group,near_chest)
        
        
        pnj1.idle()
        
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

            


       
        if Show_stats:
            fps = int(mainClock.get_fps())
            fps_text = fps_font.render(f"FPS : {fps}", True, (255, 255, 0))
            x_position = fps_font.render(f"X : {player.rect.x}", True, (255, 255, 0))
            y_position = fps_font.render(f"Y : {player.rect.y}", True, (255, 255, 0))
            screen.blit(fps_text, (800, 10))
            screen.blit(x_position,(900,10))
            screen.blit(y_position,(900,50))

        pygame.display.update()

if __name__ == "__main__":
    login()
    pygame.event.clear()
    main_menu()       # Montre le menu, attend que l'utilisateur clique sur "Jouer"
    # Vider les événements restants pour éviter le double-clic
    pygame.event.clear()
    launch_game()