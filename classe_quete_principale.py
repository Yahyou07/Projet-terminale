
import pygame

import sqlite3

# Connexion à la base (ou création si elle n'existe pas)
conn = sqlite3.connect("database/data_yahya.db")
cursor = conn.cursor()


# Création de la table Inventaire
cursor.execute("""
CREATE TABLE IF NOT EXISTS Stuff (
    pseudo TEXT,
    slot_index INTEGER,
    item_name TEXT,
    quantity INTEGER,
    PRIMARY KEY (pseudo, slot_index),
    FOREIGN KEY (pseudo) REFERENCES Login(pseudo),
    FOREIGN KEY (item_name) REFERENCES Item(name)
);

""")


# Sauvegarde et fermeture
conn.commit()
conn.close()
print("création terminé")



        