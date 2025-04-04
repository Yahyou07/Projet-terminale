import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

# Checkbox
checkbox_rect = pygame.Rect(50, 50, 20, 20)
checked = False

# Bouton
button_rect = pygame.Rect(100, 50, 100, 30)
button_text = "Clique-moi"
font = pygame.font.SysFont(None, 24)

running = True
while running:
    screen.fill((255, 255, 255))
    
    # Checkbox
    pygame.draw.rect(screen, (0, 0, 0), checkbox_rect, 2)
    if checked:
        pygame.draw.line(screen, (0, 0, 0), (checkbox_rect.left + 4, checkbox_rect.centery),
                         (checkbox_rect.centerx, checkbox_rect.bottom - 4), 2)
        pygame.draw.line(screen, (0, 0, 0), (checkbox_rect.centerx, checkbox_rect.bottom - 4),
                         (checkbox_rect.right - 4, checkbox_rect.top + 4), 2)

    # Bouton avec survol souris
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        button_color = (255, 255, 0)  # jaune
    else:
        button_color = (200, 200, 200)

    pygame.draw.rect(screen, button_color, button_rect)
    pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)
    text_surf = font.render(button_text, True, (0, 0, 0))
    screen.blit(text_surf, (button_rect.x + 5, button_rect.y + 5))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if checkbox_rect.collidepoint(event.pos):
                checked = not checked
            elif button_rect.collidepoint(event.pos):
                print("Bouton cliqué !")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
