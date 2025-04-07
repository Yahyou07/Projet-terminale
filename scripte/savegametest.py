import pygame
import sys
import sqlite3
from pygame.locals import *

class Save_game(object):
    """
        Permet de sauvegarder la partie d'un joueur en particulier
    """
    def __init__(self, ecran):
        self.screen = ecran
        self.quit = pygame.Rect(750, 0, 200, 50)
        self.parametre_btn = pygame.Rect(950, 0, 200, 50)
        self.text_quit = "Quitter la partie"
        self.text_param = "Paramètre"
        self.connexion = sqlite3.connect('save-game.db')
        self.clock = pygame.time.Clock()
        self.running = True

        self.confirm_box = pygame.Rect(250, 300, 400, 200)
        self.confirm_yes = pygame.Rect(270, 420, 160, 50)
        self.confirm_no = pygame.Rect(470, 420, 160, 50)
        
        

    def update(self):
        """
        Affiche les boutons "Quitter" et "Paramètre" en permanence
        """
        font = pygame.font.SysFont(None, 50)

        pygame.draw.rect(self.screen, (255, 255, 255), self.quit)
        pygame.draw.rect(self.screen, (0, 0, 0), self.quit, 2)
        quit_text = font.render(self.text_quit, True, (0, 0, 0))
        self.screen.blit(quit_text, (self.quit.x + 10, self.quit.y + 10))

        pygame.draw.rect(self.screen, (255, 255, 255), self.parametre_btn)
        pygame.draw.rect(self.screen, (0, 0, 0), self.parametre_btn, 2)
        param_text = font.render(self.text_param, True, (0, 0, 0))
        self.screen.blit(param_text, (self.parametre_btn.x + 10, self.parametre_btn.y + 10))

    def handle_event(self, event, joueur, level_joueur):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.quit.collidepoint(event.pos):
                print("Êtes-vous sûr de quitter ?")
                # self.sauvegarder(joueur, level_joueur)
                self.affichage_quit()
                
            elif self.parametre_btn.collidepoint(event.pos):
                print("Paramètre du jeu")
                # Affichage des paramètres ici (à développer)

    def sauvegarder(self, joueur, level_joueur):
        """
            Sauvegarde le joueur dans un fichier
            joueur : le joueur à sauvegarder
        """
        curseur = self.connexion.cursor()
        requeteSQL = "UPDATE Save SET save_level = {} WHERE pseudo = '{}';".format(level_joueur, joueur)
        curseur.execute(requeteSQL)
        curseur.close()
        self.connexion.commit()
        self.connexion.close()

    def parametre(self):
        pass
    
    def affichage_quit(self):
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
