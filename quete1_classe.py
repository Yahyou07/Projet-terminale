import random
import pygame
from items import*
from classe_entity_Yahya import*
class Quete1:
    def __init__(self):
        """ Initialise la quête avec des objectifs à remplir """
        self.etapes = {
            "Départ": {"objectif": "ramasser 10 morceaux de bois", "action": self.ramasser_bois, "suivant": "Revenir"},
            "Revenir": {"objectif": "revenir parler à ...", "action": self.revenir_parler, "suivant": "Victoire"},
            "Victoire": {"objectif": None, "action": None, "suivant": None}
        }
        
        self.descriptions = {
            "Départ": "Le village a besoin de bois.",
            "Revenir": "Revenez parler au PNJ pour lui dire que vous avez fini votre mission.",
            "Victoire": "Félicitations ! Vous avez accompli votre mission avec succès."
        }
        
        self.position_actuelle = "Départ"
    
    def ramasser_bois(self):
        pass

    def revenir_parler(self):
        pass

    def avancer(self):
        """ Passe à l'étape suivante """
        etape = self.etapes[self.position_actuelle]
        if etape["suivant"]:
            self.position_actuelle = etape["suivant"]

class GestionnaireQuete:
    def __init__(self, quete):
        self.quete = quete
        self.font = pygame.font.Font(None, 28)
        self.bois = 0
        self.parler_pnj = False
        self.messages = []  # Messages ponctuels
        self.bois_message = ""  # Message spécial bois
        self.afficher_quete = False  # <- Par défaut, on n'affiche pas

    def gerer_evenements(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                     #Déclenche l'affichage au premier appui sur A
                    self.afficher_quete = True

                    if self.quete.position_actuelle == "Départ":
                        #self.bois += 1
                        self.bois_message = f"Bois ramassé : {self.bois}"
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
        """ Affiche les informations de quête uniquement si la condition est remplie """
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

# Programme principal pour tester
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("RPG - Exemple avec condition d'affichage")

    quete = Quete1()
    gestionnaire_quete = GestionnaireQuete(quete)

    clock = pygame.time.Clock()
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        gestionnaire_quete.gerer_evenements(events)

        screen.fill((30, 30, 30))  # fond sombre

        # Ici ton jeu afficherait ses trucs...

        # Puis afficher la quête uniquement si condition remplie
        gestionnaire_quete.afficher(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

