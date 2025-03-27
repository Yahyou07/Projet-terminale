import random
import pygame

class Quete:
    def __init__(self):
        """ Initialise la quête avec des objectifs à remplir """
        self.etapes = {
            "Départ": {"objectif": "tuer 5 gobelins", "action": self.tuer_gobelins, "suivant": "Explorer"},
            "Explorer": {"objectif": "obtenir 3 fois un 3 en lançant un dé", "action": self.lancer_de, "suivant": "Victoire"},
            "Victoire": {"objectif": None, "action": None, "suivant": None}
        }
        
        self.descriptions = {
            "Départ": "Le village est attaqué par des gobelins ! Vous devez les éliminer.",
            "Explorer": "Vous explorez une grotte mystérieuse et tentez votre chance avec un dé magique...",
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
    
  

    def lancer_de(self):
        """ Simule le lancer de dé où l'on doit obtenir 3 fois un 3 """
        succes = 0
        print("Appuyez sur 'E' pour lancer le dé...")
        for i in range(3):
            attente = True
            while attente:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                        resultat = random.randint(1, 6)
                        print(f"Lancer {i+1}: Vous avez obtenu {resultat}.")
                        if resultat == 3:
                            succes += 1
                        attente = False
        
        if succes >= 3:
            print("Bravo ! Vous avez obtenu 3 fois un 3.")
        else:
            print("Échec... Vous n'avez pas réussi l'objectif.")
            self.position_actuelle = "Explorer"  # Permet de réessayer
    
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
