import sqlite3
import pygame
from items import Item
# Initialisation de Pygame
pygame.init()
# Chargement de la police
font = pygame.font.Font(None, 20)  # Police par défaut, taille 20
def charger_item_depuis_nom(conn, nom_item):
    cursor = conn.cursor()
    cursor.execute("SELECT name, stack_max, regen, type FROM Item WHERE name = ?", (nom_item,))
    row = cursor.fetchone()
    if row:
        name, stack_max, regen, type_ = row
        return Item(name, stack_max, regen, 0, 0, type_)
    return None

def charger_inventaire(username):
    global font
    # Connexion à la base de données
    conn = sqlite3.connect('database/data_yahya.db')
    cursor = conn.cursor()
    # Requête pour récupérer les données de l'inventaire
    cursor.execute("SELECT slot_index, item_name, quantity FROM Inventaire WHERE pseudo = ?", (username,))
    donnees = cursor.fetchall()
    
    inventaire = [{}]*10  # 10 slots
    icones = [pygame.image.load(f"Items/slot.png")]*10  # Remplacez par vos icônes de slot
    stack = [font.render("", True, (255, 255, 255))] *10

    for slot_index, nom_item, quantite in donnees:
        item = charger_item_depuis_nom(conn, nom_item)
        if item:
            print(slot_index)
            inventaire[slot_index] = {
                "name": nom_item,
                "object": item,
                "quantity": quantite,
                "icon": item.icon  # supposé généré à l'init de Item
            }
            icones[slot_index] = item.icon
            stack[slot_index] = font.render(str(quantite), True, (255, 255, 255))
        else : 
            inventaire[slot_index] = {}
            icones[slot_index] = pygame.image.load(f"Items/slot.png")
            stack[slot_index] = font.render("", True, (255, 255, 255))
    return inventaire
print(charger_inventaire("yahya"))


        