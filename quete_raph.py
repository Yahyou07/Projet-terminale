
import pygame

class Quete:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.position_actuelle = "Départ"
    
    def afficher_texte(self, texte):
        """ Affiche un texte sur l'écran Pygame """
        #self.screen.fill((0, 0, 0))
        lignes = texte.split('\n')
        y_offset = 1200
        for ligne in lignes:
            text_surface = self.font.render(ligne, True, (255, 255, 255))
            self.screen.blit(text_surface, (100, y_offset))
            y_offset += 40
    
    def tuer_gobelins(self):
        """ Simule le combat contre 5 gobelins """
        gobelins_tues = 0
        self.afficher_texte("Le village est attaqué !\nAppuyez sur 'E' pour attaquer un gobelin...")
        while gobelins_tues < 5:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    gobelins_tues += 1
                    self.afficher_texte(f"Vous avez tué {gobelins_tues} gobelin(s) !")
        self.afficher_texte("Tous les gobelins ont été éliminés !")
        pygame.time.delay(1000)
    
    def revenir_parler(self):
        """ Action de revenir parler au PNJ """
        self.afficher_texte("Revenez parler au PNJ\nAppuyez sur 'E'...")
        fin_quete = False
        while not fin_quete:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    self.afficher_texte("Le PNJ vous remercie !")
                    pygame.time.delay(1000)
                    fin_quete = True
    
    def jouer(self):
        """ Gère la progression de la quête """
        self.tuer_gobelins()
        self.revenir_parler()
        self.afficher_texte("Félicitations !\nQuête terminée !")
        pygame.time.delay(1000)


# Exécution du programme
#if __name__ == "__main__":
   # pygame.init()
    #screen = pygame.display.set_mode((800, 600))
    #pygame.display.set_caption("RPG - Système de Quête")
    #font = pygame.font(None, 36)
    
   # quete = Quete(screen, font)
    #quete.jouer()
    
   # pygame.quit()