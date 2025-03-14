import networkx as nx
import matplotlib.pyplot as plt

# Création du graphe
G = nx.DiGraph()

# Ajout des quêtes (nœuds)
quetes = [
    "Début du jeu", "Combat contre des gobelins", "Énigme de maths", "Exploration de la forêt", 
    "Énigme de géographie", "Combat contre un boss", "Trouver un artefact", "Énigme d'histoire", 
    "Accès au château", "Combat final"
]
G.add_nodes_from(quetes)

# Ajout des relations entre les quêtes (arêtes)
arcs = [
    ("Début du jeu", "Combat contre des gobelins"),
    ("Début du jeu", "Énigme de maths"),
    ("Combat contre des gobelins", "Exploration de la forêt"),
    ("Énigme de maths", "Exploration de la forêt"),
    ("Exploration de la forêt", "Énigme de géographie"),
    ("Exploration de la forêt", "Combat contre un boss"),
    ("Énigme de géographie", "Trouver un artefact"),
    ("Combat contre un boss", "Trouver un artefact"),
    ("Trouver un artefact", "Énigme d'histoire"),
    ("Énigme d'histoire", "Accès au château"),
    ("Accès au château", "Combat final")
]
G.add_edges_from(arcs)

# Dessin du graphe
plt.figure(figsize=(10, 6))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=3000, font_size=10, font_weight='bold')
plt.title("Graphe des Quêtes")
plt.show()