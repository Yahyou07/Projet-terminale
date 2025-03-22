class enigme(object):
    """
    Attribut :
        questions sous forme de dictionnaire de type: 
            questions = {"une question " : [réponseA,réponseB,réponseC,réponseD,bonneréponse]}
    """
    def __init__(self,questions : dict):
        assert type(questions) == dict , "Attention : le groupe de questions doit être un dictionnaire"
        self.questions = questions
    
    def search(self,question : str):
        """
        La question doit être un mot afin de bien parcourir le dictionnaire questions
        """
        assert type(question) == str, "Attention : la question doit être de type string"
        if not question in self.questions:
            return None # on renvoie rien si la question mise en paramètre n'est pas une question proposée
        return self.questions[question][-1] # on récupère la bonne réponse
    
    def verification(self, question: str, reponse : str):
        """
        Attribut :
            question permettant de rechercher la bonne réponse
            réponse du joueur sur la question mis en paramètre
        """
        if reponse == self.search(question):
            return True
        else : return False
    
