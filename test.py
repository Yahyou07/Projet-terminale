from PIL import Image

# Ouvrir le GIF
gif = Image.open("gif.gif")

# Extraire chaque frame
for i in range(gif.n_frames):
    gif.seek(i)  # Aller à la frame i
    gif.save(f"frame_{i}.png")  # Sauvegarder l'image

print("Extraction terminée !")
