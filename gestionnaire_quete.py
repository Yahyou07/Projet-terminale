import random
import pygame
from quete1_classe import*
from player_Yahya import *

class GestionnaireQuete:
    def __init__(self, quete):
        self.quete = quete
        self.font = pygame.font.Font(None, 28)
        self.bois = 0
        self.parler_pnj = False
        self.messages = []  # Messages ponctuels
        self.bois_message = ""  # Message spécial bois
        self.afficher_quete = False  # <- Par défaut, on n'affiche pas
        self.quete_active = None  # Stocke la quête en cours

    def gerer_evenements(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                     #Déclenche l'affichage au premier appui sur A
                    self.afficher_quete = True


                    if self.quete.position_actuelle == "Départ":
                        #self.bois += 1
                        self.bois_message = f"Bois ramassé : {self.bois}"
                        #capte si l'item est du bois
                        


                        print(self.bois_message)

                        if self.bois >= 10:
                            self.quete.avancer()
                            self.messages.append("Tous les morceaux de bois ont été ramassés !")

                    elif self.quete.position_actuelle == "Revenir":
                        self.parler_pnj = True

                        if self.parler_pnj:
                            self.quete.avancer()
                            self.messages.append("Le PNJ vous remercie ! Mission accomplie.")


    def afficher(self, screen):
        """# Affiche les informations de quête uniquement si la condition est remplie """
        if not self.afficher_quete:
            return  # Ne rien faire si la quête ne doit pas s'afficher

        x_offset = screen.get_width() - 250
        y_offset = 20
        width = 230
        height = 250
        pygame.draw.rect(screen, (50, 50, 50), (x_offset - 10, y_offset - 10, width, height), border_radius=8)

        description = self.quete.descriptions.get(self.quete.position_actuelle, "")
        objectif = self.quete.etapes.get(self.quete.position_actuelle, {}).get("objectif", "")

        desc_surface = self.font.render(description, True, (255, 255, 255))
        screen.blit(desc_surface, (x_offset, y_offset))

        if objectif:
            obj_surface = self.font.render(f"Objectif : {objectif}", True, (200, 200, 200))
            screen.blit(obj_surface, (x_offset, y_offset + 30))

        if self.bois_message:
            bois_surface = self.font.render(self.bois_message, True, (180, 180, 0))
            screen.blit(bois_surface, (x_offset, y_offset + 70))

        max_messages = 5
        recent_messages = self.messages[-max_messages:]
        for i, msg in enumerate(recent_messages):
            msg_surface = self.font.render(msg, True, (180, 180, 0))
            screen.blit(msg_surface, (x_offset, y_offset + 100 + i * 25))


    def demarrer_quete(self, quete):
        """ Démarre une quête si elle n'est pas déjà active """
        if not quete.active:
            quete.demarrer()
            self.quete_active = quete
            print("Quête lancée :", quete.__class__.__name__)
        else:
            print("La quête est déjà active.")    

    def verifier_et_afficher_quete(self, event, pnj, quete):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a and getattr(pnj, 'dialogue_termine', False):
            self.quete_active = quete
            self.afficher_quete = True
            quete.demarrer()
            pnj.dialogue_termine = False  # Pour éviter relance multiple

    def afficher(self, screen):
        if self.afficher_quete and self.quete_active:
            description = self.quete_active.get_description()
            if description:
                texte = self.font.render(description, True, (255, 255, 0))
                screen.blit(texte, (screen.get_width() - texte.get_width() - 20, 20))