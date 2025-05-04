import random
import pygame
from items import*
from classe_entity_Yahya import*
from player_Yahya import*
from gestionnaire_quete import *

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
        self.active = False

    def ramasser_bois(self):
        pass

    def revenir_parler(self):
        pass

    def avancer(self):
        """ Passe à l'étape suivante """
        etape = self.etapes[self.position_actuelle]
        if etape["suivant"]:
            self.position_actuelle = etape["suivant"]

    def demarrer(self):
        self.active = True
        print("La quête a démarré")



