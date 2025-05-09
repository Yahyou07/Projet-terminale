import networkx as nx               # Pour créer et manipuler un graphe orienté
#quetes_principales.py
# Définition de la classe Quete
class Quete:
    def __init__(self, id, nom, description="", obligatoire=False):
        self.id = id                  # Identifiant unique de la quête
        self.nom = nom                # Nom de la quête (affiché au joueur)
        self.description = description  # Description de la quête
        self.obligatoire = obligatoire  # Marqueur pour signaler une quête obligatoire







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

# --- Création des quêtes sous forme d’objets ---
q1 = Quete("q1", "1 )Trouver le forgeron", "Le début de votre aventure.")
q2 = Quete("q2", "2 )Récupérer l'artefact")
q3 = Quete("q3", "3 )Éliminer les gobelins")
q4 = Quete("q4", "4 )Résoudre énigme dans un volcan")
q5 = Quete("q5", "5 )Ramasser du poulet")
q6 = Quete("q6", "6 )Explorer la forêt", obligatoire=True)
q7 = Quete("q7", "7 )Boss final")

# --- Création du graphe dirigé (les quêtes sont des nœuds, les transitions des arêtes) ---
G = nx.DiGraph()  # Graphe orienté = sens de progression

# Ajout des quêtes comme nœuds avec leurs données
for q in [q1, q2, q3, q4, q5, q6, q7]:
    G.add_node(q.id, data=q)

# Définition des connexions entre les quêtes (chemins possibles)
G.add_edge(q1.id, q2.id)  # Depuis q1, on peut aller vers q2
G.add_edge(q1.id, q3.id)  # ou vers q3
G.add_edge(q2.id, q4.id)  # q2 mène à q4
G.add_edge(q3.id, q5.id)  # q3 mène à q5
G.add_edge(q4.id, q6.id)  # q4 ou q5 mènent à q6 (quête obligatoire)
G.add_edge(q5.id, q6.id)
G.add_edge(q6.id, q7.id)  # La forêt mène au boss final

