
#découpeur de sprite sheet
from PIL import Image
import os

def decouper_sprite_sheet(chemin_sprite_sheet, dossier_sortie):
    # Charger l'image
    sprite_sheet = Image.open(chemin_sprite_sheet)
    largeur, hauteur = sprite_sheet.size

    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(dossier_sortie, exist_ok=True)

    compteur = 0
    for y in range(0, hauteur, 64):
        for x in range(0, largeur, 64):
            # Découper une image 64x64
            morceau = sprite_sheet.crop((x, y, x + 64, y + 64))
            morceau.save(os.path.join(dossier_sortie, f"frame{compteur}.png"))
            compteur += 1

    print(f"{compteur} sprites enregistrés dans {dossier_sortie}")

# Exemple d'utilisation
decouper_sprite_sheet("enemy/explosion.png", "enemy")
