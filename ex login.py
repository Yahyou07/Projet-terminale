import pygame
import sys
from login_class import *
pygame.init()

import json

# Supposons que row[9] vienne de la base et contient :
row = [{}, {}, '[[3, 2], [1, 5]]']

stacks_principal = json.loads(row[2])

print(stacks_principal)  # Résultat : [[3, 2], [1, 5]] (type : list de list)
'''
# Fonction de connexion simulée
def on_login():
    print("Nom d'utilisateur:", username_box.text)
    print("Mot de passe:", password_box.text)
 
# Création des éléments
username_box = InputBox(200, 120, 200, 40)
password_box = InputBox(200, 180, 200, 40, is_password=True)
login_button = Button(250, 250, 100, 40, "Se connecter", on_login)
 
# Boucle principale
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BG_COLOR)
 
    # Événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        username_box.handle_event(event)
        password_box.handle_event(event)
        login_button.handle_event(event)
 
    login_button.update()
 
    # Dessin
    title = TITLE_FONT.render("Connexion", True, TEXT_COLOR)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 40))
 
    username_box.draw(screen)
    password_box.draw(screen)
    login_button.draw(screen)
 
    label_user = FONT.render("Nom d'utilisateur:", True, TEXT_COLOR)
    label_pass = FONT.render("Mot de passe:", True, TEXT_COLOR)
    screen.blit(label_user, (200, 95))
    screen.blit(label_pass, (200, 155))
 
    pygame.display.flip()
    clock.tick(30)
 
pygame.quit()
sys.exit()
'''