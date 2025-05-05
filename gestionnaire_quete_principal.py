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

    def afficher_interface_quete(self, screen, police):
        """Affiche un petit panneau de la quête, adapté à n'importe quelle résolution."""
        if not (self.active and self.quete_principale):
            return

        sw, sh = screen.get_width(), screen.get_height()

        # Marges dynamiques : 2% de l'écran
        margin_x = int(sw * 0.02)
        margin_y = int(sh * 0.02)

        # Largeur du panneau = 30% de la largeur d'écran
        panel_width = int(sw * 0.30)

        # Position en haut à droite
        x = sw - panel_width - margin_x
        y = margin_y

        # Espacement entre lignes = 1.2 * hauteur d'une ligne de police
        line_height = int(police.get_linesize() * 1.2)

        # --- Titre ---
        titre_surf = police.render("Quête principale", True, (255, 255, 255))
        screen.blit(titre_surf, (x, y))
        y += line_height

        # --- Contenu ---
        quete = self.quete_principale
        if not quete.quete_terminee:
            etape = quete.get_etape_courante()
            desc = etape.description if etape else "<Aucune étape>"
            # On pourrait découper si desc est trop long :
            max_chars = int(panel_width / (police.size("M")[0] or 1))  # approx cols
            lines = [desc[i:i+max_chars] for i in range(0, len(desc), max_chars)]
            for line in lines:
                surf = police.render(f"- {line}", True, (200, 200, 200))
                screen.blit(surf, (x, y))
                y += line_height
        else:
            fin_surf = police.render("✓ Terminée !", True, (100, 255, 100))
            screen.blit(fin_surf, (x, y))