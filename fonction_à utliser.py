import pygame
import math

pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Paramètres
fill_time = 3.0 # Durée du remplissage
progress = 0.0
progressing = False
finished_time = 0
show_message = False

running = True
while running:
    # Affichage
    screen.fill((30, 30, 30))
    dt = clock.tick(60) / 1000  # Temps écoulé en secondes

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clic droit maintenu
    if pygame.mouse.get_pressed()[2]:
        if not progressing:
            progressing = True
            progress = 0.0
        else:
            progress += dt / fill_time
            if progress >= 1.0:
                progressing = False
                show_message = True
                finished_time = pygame.time.get_ticks()
    else:
        if progress < 1.0:
            progressing = False
            progress = 0.0

    

    if progressing:
        center = (200, 200)
        radius = 50
        end_angle = -math.pi / 2 + progress * 2 * math.pi
        pygame.draw.circle(screen, (100, 100, 100), center, radius, 5)
        pygame.draw.arc(screen, (0, 200, 0),(center[0] - radius, center[1] - radius, radius * 2, radius * 2),-math.pi / 2, end_angle, 5)

    # Afficher "Processus terminé" pendant 1 seconde
    if show_message:
        if pygame.time.get_ticks() - finished_time < 1000:
            text = font.render("Processus terminé", True, (255, 255, 255))
            rect = text.get_rect(center=(200, 300))
            screen.blit(text, rect)
        else:
            show_message = False

    pygame.display.flip()

pygame.quit()
