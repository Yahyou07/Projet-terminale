# gestionnaire_quete_principal.py

from quete_principale import QuetePrincipale

class GestionnairePrincipale:
    def __init__(self, map_actuelle):
        self.quete_principale = None
        self.map_actuelle = map_actuelle
        self.active = False

    def lancer_quete(self):
        if not self.active:
            self.quete_principale = QuetePrincipale(
                map_associee=self.map_actuelle,
                recompenses=["épée antique", "500 XP"]
            )
            self.active = True
            print("[Gestionnaire] Quête principale lancée.")
            self.quete_principale.afficher_etape()

    def annuler_quete(self):
        if self.active:
            print("[Gestionnaire] Quête principale annulée.")
            self.quete_principale = None
            self.active = False

    def etape_suivante(self):
        if self.quete_principale and not self.quete_principale.est_terminee():
            self.quete_principale.avancer()
            self.quete_principale.afficher_etape()
        elif self.quete_principale and self.quete_principale.est_terminee():
            print("[Gestionnaire] Quête principale déjà terminée.")

    def etat_actuel(self):
        if self.active:
            self.quete_principale.afficher_etape()
        else:
            print("[Gestionnaire] Aucune quête principale active.")

    def afficher_interface_quete(screen, police, quete):
        """Affiche l'étape actuelle de la quête sur l'écran du jeu"""
        if quete and not quete.quete_terminee:
            # Récupère l'étape actuelle
            etape = quete.get_etape_courante()
            if etape:
                # Texte à afficher
                titre = f"Quête principale"
                description = f"- {etape.description}"

                # Rendu du texte
                titre_texte = police.render(titre, True, (255, 255, 255))  # Jaune
                description_texte = police.render(description, True, (255, 255, 255))  # Blanc

                # Affichage à l'écran (coin haut gauche)
                screen.blit(titre_texte, (600, 600))
                screen.blit(description_texte, (600, 600))
        elif quete and quete.quete_terminee:
            fin_texte = police.render("Quête principale terminée !", True, (0, 255, 0))
            screen.blit(fin_texte, (600, 600))
