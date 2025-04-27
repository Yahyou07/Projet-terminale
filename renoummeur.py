import os

# Dossier contenant les fichiers
folder_path = "enemy/slime/walk/walk6"

# Nouveau préfixe
new_prefix = "right"

# Récupérer et trier les fichiers concernés
files = sorted([f for f in os.listdir(folder_path) if f.endswith((".png", ".jpg", ".jpeg"))])

# Renommer en partant de 1
for i, filename in enumerate(files, start=1):
    extension = os.path.splitext(filename)[1]
    new_name = f"{new_prefix}{i}{extension}"
    old_file = os.path.join(folder_path, filename)
    new_file = os.path.join(folder_path, new_name)
    os.rename(old_file, new_file)
    print(f"Renommé {filename} en {new_name}")
