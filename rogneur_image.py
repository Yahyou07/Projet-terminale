import os
from PIL import Image

def crop_center(image, target_width, target_height):
    width, height = image.size
    left = (width - target_width) // 2
    top = (height - target_height) // 2
    right = left + target_width
    bottom = top + target_height
    return image.crop((left, top, right, bottom))

def crop_images_in_folder(input_folder, output_folder, target_width, target_height):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path)
            cropped_img = crop_center(img, target_width, target_height)
            output_path = os.path.join(output_folder, filename)
            cropped_img.save(output_path)
            print(f"Image {filename} rognée et sauvegardée.")

# Exemple d'utilisation
input_folder = 'enemy/gobelin_epee/idle'          # Dossier d'entrée
output_folder = 'enemy/gobelin_epee/idle' # Dossier de sortie
target_width = 128                # Largeur voulue
target_height = 128               # Hauteur voulue

crop_images_in_folder(input_folder, output_folder, target_width, target_height)
