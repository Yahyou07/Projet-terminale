import re
class enigme(object):
    """
    Attribut :
        questions sous forme de dictionnaire de type: 
            questions = {"question (numéro):  ?" : ["réponseA : ","réponseB : ","réponseC : ","réponseD : ","bonneréponse : "]}
    """
    def __init__(self,questions : str):
        self.questions = questions #il faut que les questions soient de type string afin de vérifier si le futur dictionnaire souhaité respecte la structure souhaitée
        self.enigmes = self.verif_dico() #dictionnaire construit à l'aide de la méthode vérification de 

    def verif_dico(self):
        """
        Vérifie si les questions sont de la structure demandée et construit le dictionnaire s'il le respecte sinon il n'y aura pas de groupe d'énigmes.
        """
        pattern = r"'question (\d+) : ([^']+)'\s*:\s*\[\s*'réponse A : ([^']+)',\s*'réponse B : ([^']+)',\s*'réponse C : ([^']+)',\s*'réponse D : ([^']+)',\s*'bonne réponse : ([^']+)'\s*\]"
        
        matches = re.findall(pattern, self.questions)
        
        if matches:
            print("Structure valide!")
            self.enigmes = {}

            for match in matches:
                question_num = match[0]  # Numéro de la question
                question_text = match[1]  # Texte de la question
                question_key = f"question {question_num} : {question_text}"  # Clé complète

                reponses = [
                    f"réponse A : {match[2]}",
                    f"réponse B : {match[3]}",
                    f"réponse C : {match[4]}",
                    f"réponse D : {match[5]}",
                    f"bonne réponse : {match[6]}"
                ]

                self.enigmes[question_key] = reponses  # Ajout au dictionnaire

            return self.enigmes  # Retourne un dictionnaire avec toutes les questions
        else:
            print("Structure invalide.")
            return None

    def obtenir_enigmes(self) : return self.enigmes

    def search(self,question : str):
        """
        La question doit être un mot afin de bien parcourir le dictionnaire questions
        """
        assert type(question) == str, "Attention : la question doit être de type string"
        if not question in self.enigmes:
            return None # on renvoie rien si la question mise en paramètre n'est pas une question proposée
        return self.enigmes[question][-1] # on récupère la bonne réponse
    
    def verification(self, question: str, reponse : str):
        """
        Attribut :
            question permettant de rechercher la bonne réponse
            réponse du joueur sur la question mis en paramètre
        """
        if reponse == self.search(question):
            return True
        else : return False
    
dico = """{
    'question 1 : Qui est le singe' : ['réponse A : Tu es fous','réponse B : Tu es fouuu','réponse C : Tu es picece','réponse D : rhgreg','bonne réponse : Tu es fous'],
    'question 2 : Quelle est la couleur du ciel ?' : ['réponse A : Rouge','réponse B : Bleu','réponse C : Vert','réponse D : Noir','bonne réponse : Bleu']
}"""

print(enigme(dico).verification('question 2 : Quelle est la couleur du ciel ?','réponse A : Rouge'))