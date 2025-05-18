
import pygame

import sqlite3

# Connexion à la base (ou création si elle n'existe pas)
conn = sqlite3.connect("database/data_yahya.db")
cursor = conn.cursor()


# Création de la table Inventaire
cursor.execute("""

CREATE TABLE IF NOT EXISTS InventairePrincipal (
    pseudo TEXT,
    row INTEGER,
    col INTEGER,
    item_name TEXT,
    quantity INTEGER,
    PRIMARY KEY (pseudo, row, col),
    FOREIGN KEY (pseudo) REFERENCES Login(pseudo)
);
""")


# Sauvegarde et fermeture
conn.commit()
conn.close()
print("création terminé")



        