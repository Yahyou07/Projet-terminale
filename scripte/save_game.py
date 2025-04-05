import pygame

class Save_game(object):
    """
        Permet de sauvegarder la partie d'un joueur en particulier
    """
    def __init__(self,ecran):
        self.screen = ecran
        self.quit = pygame.Rect(750, 0, 100, 30)
        self.running = True


    def affiche(self):
        font_quit = pygame.font.SysFont(None,50)
        self.text = "X"

        while self.running:

            pygame.draw.rect(self.screen, (255,255,255), self.quit)
            pygame.draw.rect(self.screen, (0, 0, 0), self.quit, 2)
            text_surf = font_quit.render(self.text, True, (0, 0, 0))
            self.screen.blit(text_surf, (self.quit.x + 5, self.quit.y + 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.quit.collidepoint(event.pos):
                        print("êtes vous sûr de quitter ?")

