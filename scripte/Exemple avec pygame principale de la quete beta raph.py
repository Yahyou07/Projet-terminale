import random
import pygame 

class Quete:
    def __init__(self):
        """ Initialise la quête avec des objectifs à remplir """
        self.etapes = {
            "Départ": {"objectif": "tuer 5 gobelins", "action": self.tuer_gobelins, "suivant": "Revenir"},
            "Revenir": {"objectif": "revenir parler à ...", "action": self.revenir_parler, "suivant": "Victoire"},
            "Victoire": {"objectif": None, "action": None, "suivant": None}
        }
        
        self.descriptions = {
            "Départ": "Le village est attaqué par des gobelins ! Vous devez les éliminer.",
            "Revenir": "Revenez parler au PNJ pour lui dire que vous avez fini votre mission.",
            "Victoire": "Félicitations ! Vous avez accompli votre mission avec succès."
        }
        
        self.position_actuelle = "Départ"
    
    def tuer_gobelins(self):
        """ Simule le combat contre 5 gobelins """
        gobelins_tues = 0
        print("Appuyez sur 'E' pour attaquer un gobelin...")
        while gobelins_tues < 5:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    gobelins_tues += 1
                    print(f"Vous avez tué {gobelins_tues} gobelin(s) !")
        print("Tous les gobelins ont été éliminés !")
    
    def revenir_parler(self):
        """ Action de revenir parler au PNJ pour confirmer la fin """
        fin_quete = False
        print("Appuyez sur 'E' pour aller parler au PNJ..")
        while fin_quete == False:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    print("Le PNJ vous remercie !")
                    fin_quete = True            
    
    def avancer(self):
        """ Fait progresser la quête une fois l'objectif atteint """
        etape = self.etapes[self.position_actuelle]
        print(f"\n{self.descriptions[self.position_actuelle]}")
        if etape["objectif"]:
            print(f"Objectif : {etape['objectif']}")
            etape["action"]()
        
        if etape["suivant"]:
            self.position_actuelle = etape["suivant"]
        else:
            print("Quête terminée !")

def jouer_quete(quete):
    """ Boucle principale du jeu qui permet au joueur de progresser dans une quête """
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("RPG - Système de Quête")
    
    while quete.etapes[quete.position_actuelle]["suivant"]:
        quete.avancer()
    
    print(f"\n{quete.descriptions[quete.position_actuelle]} Fin de la quête.")
    pygame.quit()

# Exécution du programme
if __name__ == "__main__":
    quete = Quete()
    jouer_quete(quete)
