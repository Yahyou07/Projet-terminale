# gestionnaire_quete_principal.py

from quete_principale import QuetePrincipale

class GestionnairePrincipale:
    def __init__(self, map_actuelle):
        # map_actuelle est simplement le nom ou l’identifiant de ta carte
        self.map_actuelle = map_actuelle
        self.quete_principale = None
        self.active = False

        self.compteur_buches = 0
        self.buches_requises = 10


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
        if not (self.active and self.quete_principale):
            return

        sw, sh = screen.get_size()
        margin_x = int(sw * 0.02)
        margin_y = int(sh * 0.02)
        panel_w  = int(sw * 0.30)
        x = sw - panel_w - margin_x
        y = margin_y
        line_h = int(police.get_linesize() * 1.2)

        # Titre
        titre = police.render("Quête principale", True, (255,255,255))
        screen.blit(titre, (x, y)); y += line_h

        qp = self.quete_principale
        if not qp.est_terminee():
            et = qp.get_etape_courante()
            desc = et.description if et else "<aucune étape>"
            # on découpe desc si elle est trop longue...
            max_chars = max(10, panel_w // (police.size("M")[0] or 1))
            for i in range(0, len(desc), max_chars):
                segment = desc[i:i+max_chars]
                seg_surf = police.render(f"- {segment}", True, (200,200,200))
                screen.blit(seg_surf, (x, y)); y += line_h

            # ⇨ **NOUVEAU** : si on est à l'étape de bois (id "2"), afficher le compteur
            if qp.etape_courante_id == "2":
                prog = f"Bois : {self.compteur_buches}/{self.buches_requises}"
                prog_surf = police.render(prog, True, (255,200,0))
                # on peut le mettre juste en dessous :
                screen.blit(prog_surf, (x, y)); y += line_h

        else:
            fin = police.render("✓ Terminée !", True, (100,255,100))
            screen.blit(fin, (x, y))


    def collecter_objet(self, objet):
        """
        Appelé à chaque ramassage : n'avance la quête
        que si objet.name == 'buche1' et qu'on est à l'étape de bois.
        """
        # On ne fait rien si la quête n'est pas active ou déjà finie
        if not (self.active and self.quete_principale and not self.quete_principale.est_terminee()):
            return

        # Vérifier qu'on est bien à l'étape « Ramasser du bois » (ex id "2")
        if self.quete_principale.etape_courante_id == "2" and objet.name == "buche1":
            self.compteur_buches += 1
            print(f"Bûches collectées : {self.compteur_buches}/{self.buches_requises}")

            # Si on a assez de bois, passer à l'étape suivante
            if self.compteur_buches >= self.buches_requises:
                self.quete_principale.avancer()
                print("Étape bois terminée : on passe à la suivante !")

    def couper_arbre(self):
        """
        À appeler dès qu'un arbre (Tronc) est effectivement coupé.
        Permet de passer de l'étape 1 (« parlez au chef ») à l'étape 2 (« ramasser du bois »).
        """
        # 1) Vérifier que la quête est active et qu'on est à l'étape 1
        if not (self.active and
                self.quete_principale and
                not self.quete_principale.est_terminee() and
                self.quete_principale.etape_courante_id == "1"):
            return

        # 2) On passe à l'étape suivante
        self.quete_principale.avancer()
        print("Étape 1 accomplie : vous avez coupé un arbre, passez à l'étape 2 !")