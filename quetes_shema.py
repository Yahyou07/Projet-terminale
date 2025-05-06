import networkx as nx
import matplotlib.pyplot as plt
class Quete:
    def __init__(self, id, nom, description="", obligatoire=False):
        self.id = id
        self.nom = nom
        self.description = description
        self.obligatoire = obligatoire

    def __repr__(self):
        return self.nom

# Création des quêtes
q1 = Quete("q1", "Trouver le forgeron", "Le début de votre aventure.")
q2 = Quete("q2", "Récupérer l'artefact")
q3 = Quete("q3", "Éliminer les gobelins")
q4 = Quete("q4", "resoudre enigme dans un volcan ")
q5 = Quete("q5", "ramasse du poulet")
q6 = Quete("q6", "Explorer la forêt", obligatoire=True)
q7 = Quete("q7", "Boss final")

# Graphe orienté
G = nx.DiGraph()
for q in [q1, q2, q3, q4, q5,q6,q7]:
    G.add_node(q.id, data=q)

# Connexions
G.add_edge(q1.id, q2.id)
G.add_edge(q1.id, q3.id)
G.add_edge(q2.id, q4.id)
G.add_edge(q3.id, q5.id)
G.add_edge(q4.id, q6.id)
G.add_edge(q5.id, q6.id)
G.add_edge(q6.id, q7.id)


# Simulation
def jouer_quetes(graphe, depart_id):
    current_id = depart_id
    while True:
        quete = graphe.nodes[current_id]["data"]
        print(f"\n***Quête : {quete.nom} ***")
        if quete.description:
            print(f"Description : {quete.description}")
        
        # Validation avec "o"
        while True:
            val = input("Tape 'o' pour valider cette quête : ").lower()
            if val == "o":
                break
        
        # Prochaines quêtes
        suivants = list(graphe.successors(current_id))
        if not suivants:
            print("Tu as terminé toutes les quêtes. Bravo !")
            break
        elif len(suivants) == 1:
            next_id = suivants[0]
            print(f"Suite obligatoire : {graphe.nodes[next_id]['data'].nom}")
        else:
            print("Choisis la quête suivante :")
            for i, sid in enumerate(suivants):
                print(f"{i+1}. {graphe.nodes[sid]['data'].nom}")
            while True:
                try:
                    choix = int(input("Ton choix (1/2...) : "))
                    if 1 <= choix <= len(suivants):
                        next_id = suivants[choix - 1]
                        break
                except:
                    pass
                print("Choix invalide.")
        current_id = next_id

# Récupérer les noms pour l'affichage
labels = {node: G.nodes[node]['data'].nom for node in G.nodes}

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightgreen', node_size=2500, font_size=9, arrowsize=20)
plt.title("Graphe des Quêtes (Objets)")
plt.show()
# Lancer
jouer_quetes(G, "q1")
