import networkx as nx               # Pour créer et manipuler un graphe orienté
#quetes_principales.py
# Définition de la classe Quete

class Quete:
    def __init__(self, id, nom, description):
        self.id = id
        self.nom = nom
        self.description = description
        self.active = False
        self.terminee = False
        








class Quest_Manager:
    def __init__(self, graphe):
        self.graphe = graphe
        self.quetes_actives = []

    def peut_demarrer(self, id_quete):
        # On vérifie que toutes les quêtes précédentes sont terminées
        prerequis = list(self.graphe.predecessors(id_quete))
        return all(self.graphe.nodes[q]['quete'].terminee for q in prerequis)

    def demarrer_quete(self, id_quete):
        quete = self.graphe.nodes[id_quete]['quete']
        if self.peut_demarrer(id_quete) and not quete.terminee:
            quete.demarrer()
            self.quetes_actives.append(quete)

    def terminer_quete(self, id_quete):
        quete = self.graphe.nodes[id_quete]['quete']
        quete.terminer()
        self.quetes_actives.remove(quete)

    def quetes_disponibles(self):
        # Renvoie les quêtes prêtes à être proposées
        disponibles = []
        for node in self.graphe.nodes:
            quete = self.graphe.nodes[node]['quete']
            if not quete.active and not quete.terminee and self.peut_demarrer(node):
                disponibles.append(quete)
        return disponibles



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


