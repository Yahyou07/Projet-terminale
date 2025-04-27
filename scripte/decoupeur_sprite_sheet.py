'''
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
    for y in range(0, hauteur, 32):
        for x in range(0, largeur, 32):
            # Découper une image 64x64
            morceau = sprite_sheet.crop((x, y, x + 32, y + 32))
            morceau.save(os.path.join(dossier_sortie, f"sprite_{compteur}.png"))
            compteur += 1

    print(f"{compteur} sprites enregistrés dans {dossier_sortie}")

# Exemple d'utilisation
decouper_sprite_sheet("enemy/slime.png", "enemy")
'''
#renommeur :
import os

# Dossier contenant les fichiers à renommer
folder_path = "enemy/slime/walk/walk1"

# Nouveau préfixe
new_prefix = "right"

# Parcours des fichiers du dossier
for filename in os.listdir(folder_path):
    if filename.startswith("sprite") and filename.endswith((".png", ".jpg", ".jpeg")):
        # Extraire le numéro après le _
        parts = filename.split("_")
        if len(parts) > 1:
            number = parts[1].split('.')[0]
            extension = os.path.splitext(filename)[1]
            new_name = f"{new_prefix}{number}{extension}"
            old_file = os.path.join(folder_path, filename)
            new_file = os.path.join(folder_path, new_name)
            os.rename(old_file, new_file)
            print(f"Renommé {filename} en {new_name}")
