import re
class enigme(object):
    """
    Attribut :
        questions sous forme de dictionnaire de type: 
            questions = {"question (numéro):  ?" : ["réponseA : ","réponseB : ","réponseC : ","réponseD : ","bonneréponse : "]}
    """
    def __init__(self,questions : str):
        self.questions = questions
        self.enigmes = None

    def verif_dico(self):
        """
        Vérifie si les questions sous forme de dictionnaire et extrait correctement la question dans la clé.
        """
        pattern = r"^\{\s*'question (\d+) : ([^']+)'\s*:\s*\[\s*'réponse A : ([^']+)',\s*'réponse B : ([^']+)',\s*'réponse C : ([^']+)',\s*'réponse D : ([^']+)',\s*'bonne réponse : ([^']+)'\s*\]\s*\}$"
        
        match = re.match(pattern, self.questions)
        
        if match:
            print("Structure valide!")
            question_num = match.group(1)  # Numéro de la question
            question_text = match.group(2)  # Texte de la question
            question_key = f"question {question_num} : {question_text}"  # Clé complète avec numéro et texte
            
            reponses = [
                f'réponse A : {match.group(3)}',
                f'réponse B : {match.group(4)}',
                f'réponse C : {match.group(5)}',
                f'réponse D : {match.group(6)}',
                f'bonne réponse : {match.group(7)}'
            ]
            
            return {question_key: reponses}  # Retourne un dictionnaire avec la clé complète
        else:
            print("Structure invalide.")
            return None


    def obtenir_enigmes(self): return self.enigmes


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
    
dico = "{'question 1 : Qui est le singe?' : ['réponse A : Tu es fous','réponse B : Tu es fouuu','réponse C : Tu es picece','réponse D : rhgreg','bonne réponse : Tu es fous']}"

print(enigme(dico).verif_dico())