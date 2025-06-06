import pygame
import sys
import sqlite3
from pygame.locals import *

class Save_game_y(object):
    """
        Permet de sauvegarder la partie d'un joueur en particulier
        Attributs:
            ecran : l'écran de jeu
    """
    def __init__(self, ecran):
        self.screen = ecran
        self.image = pygame.image.load("UI/pause.png")
        self.largeur, self.hauteur = self.screen.get_size() #récuparation de la taille de l'écran
    
        self.quit = pygame.image.load("UI/quit.png")
        self.retour = pygame.image.load("UI/return_game.png")

        self.activate = pygame.image.load("UI/activate.png") # état du bouton activer
        self.desactivate = pygame.image.load("UI/disactivate.png") # état du bouton désactiver
        self.activation_temp = self.activate  # Variable pour stocker l'état du bouton d'activation

        self.quit_rect = self.quit.get_rect(topleft=((self.largeur-768)//2+390,(self.hauteur-512)//2+337))  # Met à jour la position du bouton quitter
        self.retour_rect = self.retour.get_rect(topleft=((self.largeur-768)//2+125,(self.hauteur-512)//2+337))  # Met à jour la position du bouton retour
        self.activate_rect = self.activate.get_rect(topleft=((self.largeur-768)//2+456,(self.hauteur-512)//2 + 117))  # Met à jour la position du bouton activer

        self.connexion = sqlite3.connect('database/data_yahya.db')
        self.clock = pygame.time.Clock()
        self.running = True
        self.quitte = False
        
        self.confirm_box = pygame.Rect(250, 300, 400, 200)
        self.confirm_yes = pygame.Rect(270, 420, 160, 50)
        self.confirm_no = pygame.Rect(470, 420, 160, 50)

        self.music = True # Variable pour contrôler la musique

        # si la musique est activée, elle sera jouée en continue
        '''if self.music:
            pygame.mixer.music.load("music/music.mp3")
            pygame.mixer.music.set_volume(0.5)  # 0.0 (muet) à 1.0 (volume max)
            pygame.mixer.music.play(-1)  # Joue la musique en boucle
            print("Musique lancée")'''
        

    def update(self):
        """
            Affiche les boutons "Quitter" et "Paramètre" en permanence
        """
        font = pygame.font.SysFont(None, 50)
        
        
        if self.quitte:
            fond = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
            fond.fill((40, 40, 40, 200))  # Rouge avec 50% de transparence (128/255)
            self.screen.blit(fond, (0, 0))
            self.screen.blit(self.image,((self.largeur-768)//2,(self.hauteur-512)//2))
            self.screen.blit(self.quit,((self.largeur-768)//2+390,(self.hauteur-512)//2+337))
            self.screen.blit(self.retour,((self.largeur-768)//2+125,(self.hauteur-512)//2+337))
            self.screen.blit(self.activation_temp,((self.largeur-768)//2+456,(self.hauteur-512)//2 + 117))  # Affiche le bouton activé

    def handle_event(self, event, joueur : str , level_joueur : int , pos_x : int , pos_y : int ,vie : int,mana : int,endurance : int,quete_id : str ,inventory_barlist : list ,inventory_list : list,stuff_list : list,map_id :str ):
        """
            Gère les événements de la fenêtre de jeu
            event : l'événement à gérer
            joueur : le joueur à sauvegarder
            level_joueur : le niveau du joueur à sauvegarder
            pos_x : position x du joueur 
            pos_y : position y du joueur
            barre d'action du joueur : la barre d'action du joueur à sauvegarder
            inventaire : l'inventaire du joueur à sauvegarder   
        """
        if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE:
                    self.quitte = not self.quitte  # Inverse l'état de la variable self.quitte
                    #self.parametre_btn_rect = self.parametre_btn.get_rect(topleft=(self.largeur-75, 0))  # Met à jour la position du bouton paramètre
                    
        if event.type == pygame.MOUSEBUTTONDOWN and self.quitte:
            if event.button == 1:  # Si le bouton gauche de la souris est cliqué  
                if self.quit_rect.collidepoint(event.pos):
                        self.sauvegarder(joueur, level_joueur, pos_x, pos_y, vie, mana, endurance,quete_id,map_id)
                        self.sauvegarder_inventaire(joueur, inventory_barlist)
                        self.sauvegarder_inventaire_principal(joueur,inventory_list)
                        self.sauvegarder_stuff(joueur,stuff_list)
                        pygame.mixer.music.stop()  # Arrête la musique
                        self.running = False

                elif self.retour_rect.collidepoint(event.pos):
                        self.return_game()
                elif self.activate_rect.collidepoint(event.pos):
                    self.music = not self.music  # Inverse l'état de la musique
                    if self.music:
                        pygame.mixer.music.unpause()  # Reprend la musique si elle était en pause
                        self.activation_temp = self.activate  # Met à jour l'état du bouton d'activation
                        print("Musique activée")
                    if not self.music:
                        pygame.mixer.music.pause()
                        self.activation_temp = self.desactivate
                        print("Musique désactivée")
                        
                

    def sauvegarder(self, joueur : str , level_joueur : int , pos_x : int , pos_y : int ,vie : int,mana : int,endurance : int, quete_id : str,map_id : str):
        """
            Sauvegarde le joueur dans un fichier
            joueur : le joueur à sauvegarder
            level_joueur : le niveau du joueur à sauvegarder
            pos_x : position x du joueur
            pos_y : position y du joueur
            barre d'action du joueur : la barre d'action du joueur à sauvegarder
            inventaire : l'inventaire du joueur à sauvegarder
        """
        curseur = self.connexion.cursor()
        requeteSQL = '''update Login set pos_x = {}, pos_y = {} , level = {},health = {},mana = {},endurance = {} where pseudo = {}'''.format(pos_x,pos_y,level_joueur,vie,mana,endurance,joueur) # rerquête à modifier afin d'enregistrer l'emplacement du joueur et le contenu de son inventaire
        curseur.execute('''update Login set pos_x = ?, pos_y = ? , level = ?,health = ?,mana = ?,endurance = ?,current_quete = ?,current_map = ? where pseudo = ?''',(pos_x,pos_y,level_joueur,vie,mana,endurance,quete_id,map_id,joueur))
        curseur.close()
        

    def sauvegarder_inventaire(self, pseudo, inventaire):
        cursor = self.connexion.cursor()

        # Supprimer les anciennes données
        cursor.execute("DELETE FROM Inventaire WHERE pseudo = ?", (pseudo,))

        # Ajouter les nouvelles données
        index = 0
        for slot in inventaire:
            if slot:
                cursor.execute("""
                    INSERT INTO Inventaire (pseudo, slot_index, item_name, quantity)
                    VALUES (?, ?, ?, ?)
                """, (pseudo, index, slot['name'], slot['quantity']))
            index += 1
        cursor.close()
        

    def sauvegarder_inventaire_principal(self, pseudo, inventaire_principal):
        cursor = self.connexion.cursor()

        # Supprimer les anciennes données
        cursor.execute("DELETE FROM InventairePrincipal WHERE pseudo = ?", (pseudo,))

        # Ajouter les nouvelles données
        row_index = 0
        for row in inventaire_principal:
            col_index = 0
            for slot in row:
                if slot:
                    cursor.execute("""
                        INSERT INTO InventairePrincipal (pseudo, row, col, item_name, quantity)
                        VALUES (?, ?, ?, ?, ?)
                    """, (pseudo, row_index, col_index, slot['name'], slot['quantity']))
                col_index += 1
            row_index += 1

        cursor.close()
        
    def sauvegarder_stuff(self,pseudo,stuff_list):
        cursor = self.connexion.cursor()

        # On supprime les anciennes données
        cursor.execute("DELETE FROM Stuff WHERE pseudo = ?", (pseudo,))

        # On ajoute les nouvelles données
        index = 0
        for slot in stuff_list:
            if slot:
                cursor.execute("""
                    INSERT INTO Stuff (pseudo, slot_index, item_name, quantity)
                    VALUES (?, ?, ?, ?)
                """, (pseudo, index, slot['name'], slot['quantity']))
            index += 1
        cursor.close()
        self.connexion.commit()
        self.connexion.close()

    def return_game(self):
        """
            fonction permettant de retourner dans le jeu
        """
        self.quitte = False

    
    """def affichage_quit(self):
        while self.running : 
            
            for event in pygame.event.get():
                if event.type == pygame.quit:
                    pygame.quit()
                    exit()

            font = pygame.font.SysFont(None, 40)
            pygame.draw.rect(self.screen, (200, 200, 200), self.confirm_box)
            pygame.draw.rect(self.screen, (0, 0, 0), self.confirm_box, 2)

            msg = font.render("Êtes-vous sûr de vouloir quitter ?", True, (0, 0, 0))
            self.screen.blit(msg, (self.confirm_box.x + 30, self.confirm_box.y + 40))

            pygame.draw.rect(self.screen, (180, 255, 180), self.confirm_yes)
            pygame.draw.rect(self.screen, (0, 0, 0), self.confirm_yes, 2)
            yes_text = font.render("Oui", True, (0, 0, 0))
            self.screen.blit(yes_text, (self.confirm_yes.x + 50, self.confirm_yes.y + 10))

            pygame.draw.rect(self.screen, (255, 180, 180), self.confirm_no)
            pygame.draw.rect(self.screen, (0, 0, 0), self.confirm_no, 2)
            no_text = font.render("Non", True, (0, 0, 0))
            self.screen.blit(no_text, (self.confirm_no.x + 50, self.confirm_no.y + 10))

            pygame.display.update()
            """
