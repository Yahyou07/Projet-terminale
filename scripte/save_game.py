import pygame
import sys
import sqlite3
from pygame.locals import*

class Save_game(object):
    """
        Permet de sauvegarder la partie d'un joueur en particulier
    """
    def __init__(self,ecran):   
        self.screen = ecran # L'écran sur lequel afficher le menu de sauvegarde
        self.quit = pygame.Rect(0, 750, 100, 30)    # Rectangle pour le bouton de sauvegarde
        self.running = True # Variable pour la boucle principale


    def affiche(self,level_joueur,joueur):
        """
            Affiche le menu de sauvegarde et du quitter
            level_joueur : le niveau du joueur 
        """
        font_quit = pygame.font.SysFont(None,50)
        self.text = "Quitter la partie"

        while self.running:

            pygame.draw.rect(self.screen, (255,255,255), self.quit)
            pygame.draw.rect(self.screen, (0, 0, 0), self.quit, 2)
            text_surf = font_quit.render(self.text, True, (0, 0, 0))
            self.screen.blit(text_surf, (self.quit.x + 5, self.quit.y + 5))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.quit.collidepoint(event.pos):
                        print("êtes vous sûr de quitter ?")
                        self.sauvegarder(joueur,level_joueur)
                        self.running = False


    def sauvegarder(self,joueur,level_joueur):  
        """
            Sauvegarde le joueur dans un fichier
            joueur : le joueur à sauvegarder
        """
         ## mise à jour du score du joueur
        connexion = sqlite3.connect('save-game.db')
        #Ouverture de la base de donnée dans laquelle nous avons stocker tous les scores
        curseur = connexion.cursor()
        requeteSQL = "UPDATE Save SET save_level = {} WHERE pseudo = '{}';".format(level_joueur,joueur) # Requête SQL pour mettre à jour le score du joueur
        # On met à jour le score du joueur dans la base de données
        curseur.execute(requeteSQL)
        curseur.close()
        connexion.commit()
        connexion.close()
        pass


    

