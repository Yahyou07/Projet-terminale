import pygame  # Importe la bibliothèque Pygame

pygame.init()  # Initialise Pygame
screen = pygame.display.set_mode((800, 600))  # Crée une fenêtre de 800x600 pixels

# Charge deux icônes et les stocke dans une liste
icons = [pygame.image.load("Items/pain_icon.png"), pygame.image.load("Items/pain_icon.png")]

# Crée un rect pour chaque icône et les positionne avec un décalage horizontal
icons_rects = []
for i in range(len(icons)):
    rect = icons[i].get_rect(topleft=(100 + i*100, 100))
    icons_rects.append(rect)

# Variables pour le drag and drop
dragging = False          # Indique si on est en train de "drag"
dragged_icon = None       # Indice de l’icône qu’on déplace
offset_x, offset_y = 0, 0 # Décalage entre la souris et le coin de l’icône (pour un déplacement fluide)

clock = pygame.time.Clock()  # Pour limiter le framerate
running = True               # Boucle principale du jeu

while running:
    screen.fill((30, 30, 30))  # Remplit l'écran avec une couleur sombre

    for event in pygame.event.get():  # Récupère les événements
        if event.type == pygame.QUIT:  # Si on ferme la fenêtre
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:  # Clic de souris
            for i in range(len(icons_rects)):  # Parcourt les icônes
                if icons_rects[i].collidepoint(event.pos):  # Si la souris est sur une icône
                    dragging = True  # Active le mode drag
                    dragged_icon = i  # Stocke l’index de l’icône
                    offset_x = icons_rects[i].x - event.pos[0]  # Calcule le décalage X
                    offset_y = icons_rects[i].y - event.pos[1]  # Calcule le décalage Y
                    break

        elif event.type == pygame.MOUSEBUTTONUP:  # Relâchement de la souris
            dragging = False
            dragged_icon = None

        elif event.type == pygame.MOUSEMOTION and dragging:  # Si on déplace la souris en mode drag
            if dragged_icon is not None:
                # Met à jour la position du rect de l'icône en suivant la souris
                icons_rects[dragged_icon].x = event.pos[0] + offset_x
                icons_rects[dragged_icon].y = event.pos[1] + offset_y

    # Affiche chaque icône à sa position actuelle
    for i in range(len(icons)):
        screen.blit(icons[i], icons_rects[i])

    pygame.display.flip()  # Met à jour l'affichage
    clock.tick(60)         # Limite à 60 FPS

pygame.quit()  # Quitte Pygame
