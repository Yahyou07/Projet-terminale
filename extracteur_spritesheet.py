from PIL import Image
import random
#Petit programme qui permet d'extraire les images d'un gif

# Ouvrir le GIF
gif = Image.open("Objects/coffre.gif")


# Extraire chaque frame
for i in range(gif.n_frames):
    gif.seek(i)  # Aller à la frame i
    gif.save(f"Objects/frame_{i}.png")  # Sauvegarder l'image

print("Extraction terminée !")






