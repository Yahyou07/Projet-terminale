import pygame
from PIL import Image, ImageTk
from customtkinter import *

root = CTk()
root.geometry("700x700")
root._set_appearance_mode("dark")

# Charger l'image en arrière-plan
background_image = Image.open("image_menu2.png")  # Remplacez par le chemin de votre image
background_photo = ImageTk.PhotoImage(background_image)

# Créer un label pour afficher l'image en arrière-plan
background_label = CTkLabel(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Créer un cadre par-dessus l'image en arrière-plan
frame = CTkFrame(master=root, fg_color="#FFFFFF", width=400, height=400)
frame.pack(expand=True)


root.mainloop()

