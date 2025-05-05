# quete_secondaire.py
class QueteSecondaire:
    def __init__(self, nom, declencheur_pnj, objectif, recompense):
        self.nom = nom
        self.pnj = declencheur_pnj
        self.objectif = objectif
        self.recompense = recompense
        self.active = False
        self.terminee = False

    def declencher(self):
        print(f"Quête secondaire '{self.nom}' lancée par {self.pnj.nom}")
        self.active = True

    def terminer(self):
        print(f"Quête '{self.nom}' terminée ! Récompense : {self.recompense}")
        self.terminee = True
