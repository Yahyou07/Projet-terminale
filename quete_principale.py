# quete_principale.py

class EtapeQuete:
    def __init__(self, id_etape, description, suivantes=None):
        self.id = id_etape
        self.description = description
        self.suivantes = suivantes if suivantes else []

class QuetePrincipale:
    def __init__(self, map_associee, recompenses):
        self.map = map_associee
        self.recompenses = recompenses
        self.etapes = {}  # dictionnaire d'étapes : id -> EtapeQuete
        self.etape_courante_id = None
        self.quete_terminee = False
        self._initialiser_quete()

    def _initialiser_quete(self):
        # Création des étapes
        self.etapes = {
            "1": EtapeQuete("1", "Aller couper des arbres", ["2"]),
            "2": EtapeQuete("2", "Récolter du bois", []),
        }
        self.etape_courante_id = "1"

    def get_etape_courante(self):
        return self.etapes.get(self.etape_courante_id)

    def avancer(self):
        if not self.etape_courante_id:
            return
        etape = self.etapes[self.etape_courante_id]
        if etape.suivantes:
            self.etape_courante_id = etape.suivantes[0]
        else:
            self.quete_terminee = True
            self.etape_courante_id = None

    def est_terminee(self):
        return self.quete_terminee

    def afficher_etape(self):
        etape = self.get_etape_courante()
        if etape:
            print(f"[Quête principale] Étape actuelle : {etape.description}")
        elif self.quete_terminee:
            print("[Quête principale] La quête est terminée ! Retourne parler au PNJ")
