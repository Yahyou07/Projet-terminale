# Import des bibliothèques
import networkx as nx               # Pour créer et manipuler un graphe orienté
import matplotlib.pyplot as plt     # Pour afficher graphiquement le graphe

# Définition de la classe Quete
class Quete:
    def __init__(self, id, nom, description="", obligatoire=False):
        self.id = id                  # Identifiant unique de la quête
        self.nom = nom                # Nom de la quête (affiché au joueur)
        self.description = description  # Description de la quête
        self.obligatoire = obligatoire  # Marqueur pour signaler une quête obligatoire

    def __repr__(self):
        return self.nom               # Affichage simplifié : montre juste le nom

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

# --- Fonction principale de navigation dans les quêtes ---
def jouer_quetes(graphe, depart_id):
    current_id = depart_id  # Commencer par le nœud de départ
    while True:
        # Récupérer la quête actuelle depuis le graphe
        quete = graphe.nodes[current_id]["data"]
        
        # Afficher les infos de la quête
        print(f"\n*** Quête : {quete.nom} ***")
        if quete.description:
            print(f"Description : {quete.description}")
        
        # Demander au joueur de valider la quête en tapant 'o'
        while True:
            val = input("Tape 'o' pour valider cette quête : ").lower()
            if val == "o":
                break
        
        # Déterminer les quêtes suivantes depuis le graphe
        suivants = list(graphe.successors(current_id))
        
        # Si aucune suite : fin du jeu
        if not suivants:
            print("Tu as terminé toutes les quêtes. Bravo !")
            break
        # Si une seule suite : suite obligatoire
        elif len(suivants) == 1:
            next_id = suivants[0]
            print(f"Suite obligatoire : {graphe.nodes[next_id]['data'].nom}")
        # Sinon : proposer un choix au joueur
        else:
            print("Choisis la quête suivante :")
            i = 1
            for sid in suivants:
                print(f"{i}. {graphe.nodes[sid]['data'].nom}")
                i += 1
            # Attente d'un choix valide
            while True:
                try:
                    choix = int(input("Ton choix (1/2...) : "))
                    if 1 <= choix <= len(suivants):
                        next_id = suivants[choix - 1]
                        break
                except:
                    pass
                print("Choix invalide.")
        # Passer à la quête choisie
        current_id = next_id

# --- Affichage visuel du graphe avec matplotlib ---
# On prépare un dictionnaire des labels à afficher (noms des quêtes)
labels = {node: G.nodes[node]['data'].nom for node in G.nodes}

# Positionnement automatique des nœuds
pos = nx.spring_layout(G)

# Dessin du graphe
nx.draw(G, pos, with_labels=True, labels=labels,
        node_color='lightgreen', node_size=2500,
        font_size=9, arrowsize=20)

# Titre du graphique
plt.title("Graphe des Quêtes (Objets)")

# Affichage
plt.show()

# --- Lancer le jeu à partir de la première quête ---
jouer_quetes(G, "q1")
