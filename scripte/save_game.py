import pygame
import sys
import sqlite3
from pygame.locals import *

class Save_game(object):
    """
        Permet de sauvegarder la partie d'un joueur en particulier
        Attributs:
            ecran : l'écran de jeu
    """
    def __init__(self, ecran):
        self.screen = ecran
        self.image = pygame.image.load("pause.png")
        self.largeur, self.hauteur = self.screen.get_size() #récuparation de la taille de l'écran
        #self.quit = pygame.Rect(self.largeur//3 + 100, self.hauteur//4 + 100, 275, 50)

        self.quit = pygame.image.load("quit.png")

        self.retour = pygame.image.load("return_game.png")

        self.quit_rect = self.quit.get_rect(topleft=((self.largeur-768)//2+390,(self.hauteur-512)//2+337))  # Met à jour la position du bouton quitter
        self.retour_rect = self.retour.get_rect(topleft=((self.largeur-768)//2+125,(self.hauteur-512)//2+337))  # Met à jour la position du bouton retour   


        #self.retour = pygame.Rect(self.largeur//3 + 100, self.hauteur//4 + 200, 275, 50)

        #self.parametre_btn = pygame.image.load("parametre.png")
        #self.parametre_btn = pygame.transform.scale(self.parametre_btn, (75,75))

        self.text_quit = "Quitter la partie"
        self.text_param = "Paramètre"
        self.text_retour = "Retourner"
        self.connexion = sqlite3.connect('save-game.db')
        self.clock = pygame.time.Clock()
        self.running = True
        self.quitte = False
        
        self.confirm_box = pygame.Rect(250, 300, 400, 200)
        self.confirm_yes = pygame.Rect(270, 420, 160, 50)
        self.confirm_no = pygame.Rect(470, 420, 160, 50)
        
        

    def update(self):
        """
        Affiche les boutons "Quitter" et "Paramètre" en permanence
        """
        font = pygame.font.SysFont(None, 50)

        if self.quitte:
            self.screen.blit(self.image,((self.largeur-768)//2,(self.hauteur-512)//2))
            """pygame.draw.rect(self.screen, (255, 255, 255), self.quit)
            pygame.draw.rect(self.screen, (0, 0, 0), self.quit, 2)
            

            pygame.draw.rect(self.screen, (255, 255, 255), self.retour)
            pygame.draw.rect(self.screen, (0, 0, 0), self.retour, 2)

            quit_text = font.render(self.text_quit, True, (0, 0, 0))
            self.screen.blit(quit_text, (self.quit.x + 5, self.quit.y + 10))

            
            retour_text = font.render(self.text_retour, True, (0, 0, 0))
            self.screen.blit(retour_text, (self.retour.x + 5, self.retour.y + 10))
            """
            self.screen.blit(self.quit,((self.largeur-768)//2+390,(self.hauteur-512)//2+337))
            self.screen.blit(self.retour,((self.largeur-768)//2+125,(self.hauteur-512)//2+337))
        #pygame.draw.rect(self.screen, (255, 255, 255), self.parametre_btn)
        #pygame.draw.rect(self.screen, (0, 0, 0), self.parametre_btn, 2)
        param_text = font.render(self.text_param, True, (0, 0, 0))
        #self.screen.blit(self.parametre_btn,(self.largeur-75, 0))
        #self.screen.blit(param_text, (self.parametre_btn.x + 10, self.parametre_btn.y + 10))

    def handle_event(self, event, joueur : str , level_joueur : int , pos_x : int = None, pos_y : int = None,inventory_barlist : list = None,invetory_list : list = None):
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
                    self.quitte = not self.quitte
                    #self.parametre_btn_rect = self.parametre_btn.get_rect(topleft=(self.largeur-75, 0))  # Met à jour la position du bouton paramètre
                    
        if event.type == pygame.MOUSEBUTTONDOWN and self.quitte:
            if event.button == 1:  # Si le bouton gauche de la souris est cliqué  
                if self.quit_rect.collidepoint(event.pos):
                        print("tu vas quitter la game chef")
                        #self.sauvegarder(joueur, level_joueur, pos_x, pos_y)
                        pygame.quit()
                        sys.exit()

                elif self.retour_rect.collidepoint(event.pos):
                        print("retour dans le jeu")
                        self.return_game()
                

    def sauvegarder(self, event, joueur : str , level_joueur : int , pos_x : int = None, pos_y : int = None,inventory_barlist : list = None,invetory_list : list = None):
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
        requeteSQL = "UPDATE Save SET save_level = {} WHERE pseudo = '{}';".format(level_joueur, joueur) # rerquête à modifier afin d'enregistrer l'emplacement du joueur et le contenu de son inventaire
        curseur.execute(requeteSQL)
        curseur.close()
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
