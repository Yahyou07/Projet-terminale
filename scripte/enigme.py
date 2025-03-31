import re
import pygame
class Enigme(object):
    """
    Attribut :
        questions sous forme de dictionnaire de type: 
            questions = {"question (numéro):  ?" : ["réponseA : ","réponseB : ","réponseC : ","réponseD : ","bonneréponse : "]}
            
    """
    def __init__(self,questions : str,screen):
        self.questions = questions #il faut que les questions soient de type string afin de vérifier si le futur dictionnaire souhaité respecte la structure souhaitée
        self.enigmes = self.verif_dico() #dictionnaire construit à l'aide de la méthode vérification du dictionnaire
        self.questionns = self.recuperation_questions()
        self.reponses = self.recuperation_reponses()
        self.screen = screen
        self.image = pygame.image.load("enigme.png")    # chargement de l'image où il y a l'énigme
        self.image = pygame.transform.scale(self.image,(790,790)) # rétrécit l'image

    def verif_dico(self):
        """
        Vérifie si les questions sont de la structure demandée et construit le dictionnaire s'il le respecte sinon il n'y aura pas de groupe d'énigmes.
        """
        pattern = r"'question (\d+) : ([^']+)'\s*:\s*\[\s*'réponse A : ([^']+)',\s*'réponse B : ([^']+)',\s*'réponse C : ([^']+)',\s*'réponse D : ([^']+)',\s*'bonne réponse : ([^']+)'\s*\]"
        
        matches = re.findall(pattern, self.questions)
        
        if matches:
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
            return None

    def obtenir_enigmes(self) : return self.enigmes

    def recuperation_questions(self):
        """
            Permet de récupérer toutes les questions dans une liste si il y a des questions
        """
        if self.enigmes != None and self.enigmes != {}:
            self.questionns = []
            for cle in self.enigmes.keys():
                self.questionns.append(cle)
            return self.questionns
        
    def recuperation_reponses(self):
        """
            Permet de récupérer toutes les réponses dans une liste s'il y a des questions
        """
        if self.enigmes != None and self.enigmes != {}:
            self.reponses = []
            for valeur in self.enigmes.values():
                self.reponses.append(valeur)
            return self.reponses
        
    
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
    
    def __str__(self):
        return str(self.enigmes)
    
    def affiche(self,n : int):
        """
            Méthode permettant d'afficher l'onglet énigme lorsqu'elle est appelée
            n étant le numéro de la question
        """
        #if self.search(question) == None : return "La question d'existe pas"

        self.screen.blit(self.image,(255,0))
        self.question = self.questionns[n-1]
        self.reponsess = self.reponses[n-1]
        fontc = pygame.font.Font(None,60)
        fontreponse = pygame.font.Font(None,30)
        questionn = fontc.render(self.question,1,(0,0,0))
        self.screen.blit(questionn,(300,50))
        reponseA = fontreponse.render(self.reponsess[0],1,(0,0,0))
        self.screen.blit(reponseA,(350,500))
        reponseB = fontreponse.render(self.reponsess[1],1,(0,0,0))
        self.screen.blit(reponseB,(750,500))
        reponseC = fontreponse.render(self.reponsess[2],1,(0,0,0))
        self.screen.blit(reponseC,(350,600))
        reponseD = fontreponse.render(self.reponsess[3],1,(0,0,0))
        self.screen.blit(reponseD,(750,600))
        




dico = """{
    'question 1 : Qui est le singe' : ['réponse A : Tu es fous','réponse B : Tu es fouuu','réponse C : Tu es picece','réponse D : rhgreg','bonne réponse : Tu es fous'],
    'question 2 : Quelle est la couleur du ciel ?' : ['réponse A : Rouge','réponse B : Bleu','réponse C : Vert','réponse D : Noir','bonne réponse : Bleu']
}"""

#print(Enigme(dico).verification('question 2 : Quelle est la couleur du ciel ?','réponse A : Rouge'))