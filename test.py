from PIL import Image

#Petit programme qui permet d'extraire les images d'un gif

# Ouvrir le GIF
gif = Image.open("UI/livre.gif")

'''
# Extraire chaque frame
for i in range(gif.n_frames):
    gif.seek(i)  # Aller à la frame i
    gif.save(f"frame_{i}.png")  # Sauvegarder l'image

print("Extraction terminée !")

'''

items = {
            "pomme":{
                "image" : 3,
                "item" : None,
                "stack_max" : 32,
                "regen" : 10,
                "effet" : None
            },
            "fish":{
                "image" : 3,
                "item" : None,
                "stack_max" : 32,
                "regen" : 10,
                "effet" : None
            }
        }



list_data = [{"pomme": 1}]
cle = list(list_data[0].keys())[0]
print(cle)  # Affichera "pomme

