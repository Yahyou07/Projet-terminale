import re
import pygame
import time

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
        

        # initialisation de tous ce qui est affichage
        self.screen = screen
        
        self.largeur, self.hauteur = self.screen.get_size() #récuparation de la taille de l'écran
        self.image = pygame.image.load("enigme.png")    # chargement de l'image où il y a l'énigme
        self.witdh, self.height = self.image.get_size() #récupération de la taille de l'image
        self.percent = 790 // self.height # pour réduire l'image à la taille de l'écran
        self.image = pygame.transform.scale(self.image,(559,790)) # rétrécit l'image
        self.Loose = False
        self.Perdu = False
        self.running = True
        self.Win = False

        #initialisation des cases à cocher
        self.case_A = pygame.Rect(350, 470, 20, 20)
        self.checked_A = False

        self.case_B = pygame.Rect(700, 470, 20, 20)
        self.checked_B = False

        self.case_C = pygame.Rect(350, 650, 20, 20)
        self.checked_C = False

        self.case_D = pygame.Rect(700, 650, 20, 20)
        self.checked_D = False

        self.reponse_joueur = ""

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
                    f"{match[2]}",
                    f"{match[3]}",
                    f"{match[4]}",
                    f"{match[5]}",
                    f"{match[6]}"
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
    
    """def affiche(self,n : int):
        
            Méthode permettant d'afficher l'onglet énigme lorsqu'elle est appelée
            n étant le numéro de la question
        
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
        
        self.temps = 10
        font_time = pygame.font.Font(None,15)
        while self.temps != 0:
            time = font_time.render(str(self.temps),1,(0,0,0))
            self.screen.blit(time,(0,0))
            self.temps -= 1
    """
    def affiche(self, n: int):
        """
        Méthode permettant d'afficher l'onglet énigme lorsqu'elle est appelée
        avec un minuteur de 10 secondes.
        """
        self.question = self.questionns[n - 1]
        self.reponsess = self.reponses[n - 1]
        self.numero_reponse = 0
        
        
        # polices de textes à afficher
        fontc = pygame.font.Font(None, 60)
        fontreponse = pygame.font.Font(None, 30)
        font_time = pygame.font.Font(None, 40)
        font_lose = pygame.font.Font(None, 50)
        
        questionn = fontc.render(self.question, True, (0, 0, 0))
        reponseA = fontreponse.render(self.reponsess[0], True, (0, 0, 0))
        reponseB = fontreponse.render(self.reponsess[1], True, (0, 0, 0))
        reponseC = fontreponse.render(self.reponsess[2], True, (0, 0, 0))
        reponseD = fontreponse.render(self.reponsess[3], True, (0, 0, 0))
        
        
        start_time = pygame.time.get_ticks()

        while self.running :
            
            if not self.Loose : 
                self.screen.blit(self.image, ((self.largeur - self.image.get_width()) // 2, (self.hauteur - self.image.get_height()) // 2))
                self.screen.blit(questionn, (300, 50))
                self.screen.blit(reponseA, (350, 500))
                self.screen.blit(reponseB, (750, 500))
                self.screen.blit(reponseC, (350, 600))
                self.screen.blit(reponseD, (750, 600))

                # checkboxs
                pygame.draw.rect(self.screen, (0, 0, 0), self.case_A, 2)
                pygame.draw.rect(self.screen, (0, 0, 0), self.case_B, 2)
                pygame.draw.rect(self.screen, (0, 0, 0), self.case_C, 2)
                pygame.draw.rect(self.screen, (0, 0, 0), self.case_D, 2)

                # si on clique sur une des cases

                if self.checked_A:
                    self.reponse_joueur = self.reponsess[0]
                    pygame.draw.line(self.screen, (0, 0, 0), (self.case_A.left + 4, self.case_A.centery),
                         (self.case_A.centerx, self.case_A.bottom - 4), 2)
                    pygame.draw.line(self.screen, (0, 0, 0), (self.case_A.centerx, self.case_A.bottom - 4),
                                    (self.case_A.right - 4, self.case_A.top + 4), 2)
                    if self.verification(self.question,self.reponse_joueur):
                        self.Win = True
                    else : self.Perdu = True

                if self.checked_B:
                    self.reponse_joueur = self.reponsess[1]
                    pygame.draw.line(self.screen, (0, 0, 0), (self.case_B.left + 4, self.case_B.centery),
                         (self.case_B.centerx, self.case_B.bottom - 4), 2)
                    pygame.draw.line(self.screen, (0, 0, 0), (self.case_B.centerx, self.case_B.bottom - 4),
                                    (self.case_B.right - 4, self.case_B.top + 4), 2)
                    if self.verification(self.question,self.reponse_joueur):
                        self.Win = True
                    else : self.Perdu = True
                
                if self.checked_C:
                    self.reponse_joueur = self.reponsess[2]
                    pygame.draw.line(self.screen, (0, 0, 0), (self.case_C.left + 4, self.case_C.centery),
                         (self.case_C.centerx, self.case_C.bottom - 4), 2)
                    pygame.draw.line(self.screen, (0, 0, 0), (self.case_C.centerx, self.case_C.bottom - 4),
                                    (self.case_C.right - 4, self.case_C.top + 4), 2)
                    if self.verification(self.question,self.reponse_joueur):
                        self.Win = True
                    else : self.Perdu = True
                    
                if self.checked_D:
                    self.reponse_joueur = self.reponsess[3]
                    pygame.draw.line(self.screen, (0, 0, 0), (self.case_D.left + 4, self.case_D.centery),
                         (self.case_D.centerx, self.case_D.bottom - 4), 2)
                    pygame.draw.line(self.screen, (0, 0, 0), (self.case_D.centerx, self.case_D.bottom - 4),
                                    (self.case_D.right - 4, self.case_D.top + 4), 2)
                    if self.verification(self.question,self.reponse_joueur):
                        self.Win = True
                    else : self.Perdu = True

                ## pour les cases, à gerer plus tard si temps
            
            pygame.display.update()
            
            if self.Perdu:
                lose_text = font_lose.render("Vous avez perdu.", True, (255, 0, 0))
                self.screen.blit(lose_text, (250, 400))
                pygame.display.update()
                time.sleep(3)
                pygame.display.update()
                self.Loose = True
                self.running = False

            ## il faudrait concevoir le fait que les questions peuvent être clicables afin de récupérer la réponse du joueur afin de la comparer à la bonne réponse 
                
            if self.Win:
                win_text = font_lose.render("Vous avez la bonne réponse.",True,(0,255,0))
                self.screen.blit(win_text,(250,400))
                pygame.display.update()
                time.sleep(3)
                pygame.display.update()
                self.Loose = True
                self.running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.case_A.collidepoint(event.pos):
                        self.checked_A = not self.checked_A
                    if self.case_B.collidepoint(event.pos):
                        self.checked_B = not self.checked_B
                    if self.case_C.collidepoint(event.pos):
                        self.checked_C = not self.checked_C
                    if self.case_D.collidepoint(event.pos):
                        self.checked_D = not self.checked_D
        
            


class VieouMort(object):
    """
        Ce sont des énigmes dont il faudra y répondre dans un temps imparti
        attribut :
            questions en string
            écran
    """
    def __init__(self,questions : str,screen):
        self.questions = questions #il faut que les questions soient de type string afin de vérifier si le futur dictionnaire souhaité respecte la structure souhaitée
        self.enigmes = self.verif_dico() #dictionnaire construit à l'aide de la méthode vérification du dictionnaire
        self.questionns = self.recuperation_questions()
        self.reponses = self.recuperation_reponses()

        # initialisation de tous ce qui est affichage
        self.screen = screen
        self.image = pygame.image.load("enigme.png")    # chargement de l'image où il y a l'énigme
        self.image = pygame.transform.scale(self.image,(790,790)) # rétrécit l'image
        self.Loose = False
        self.Perdu = False
        self.running = True
        self.Win = False

        #initialisation des cases à cocher
        self.case_A = pygame.Rect(350, 470, 20, 20)
        self.checked_A = False

        self.case_B = pygame.Rect(700, 470, 20, 20)
        self.checked_B = False

        self.case_C = pygame.Rect(350, 650, 20, 20)
        self.checked_C = False

        self.case_D = pygame.Rect(700, 650, 20, 20)
        self.checked_D = False

        self.reponse_joueur = "" 

    def verif_dico(self):
        """
        Vérifie si les questions sont de la structure demandée et construit le dictionnaire s'il le respecte sinon il n'y aura pas de groupe d'énigmes.
        """
        pattern = r"'question vie ou mort (\d+) : ([^']+)'\s*:\s*\[\s*'réponse A : ([^']+)',\s*'réponse B : ([^']+)',\s*'réponse C : ([^']+)',\s*'réponse D : ([^']+)',\s*'bonne réponse : ([^']+)'\s*\]"
        
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
    
    #def temps(self):
        #self.debut = time.time()
        #self.fin = time.time()
        #self.temp = self.fin -self.debut
        #if self.temp == 10:
            #return self.temp
        #else:
            #while self.temp != 10:
                #self.debut = time.time()
                #self.fin = time.time()
            #return self.temp
        

    
    def affiche(self, n: int):
        """
        Méthode permettant d'afficher l'onglet énigme lorsqu'elle est appelée
        avec un minuteur de 10 secondes.
        """
        self.question = self.questionns[n - 1]
        self.reponsess = self.reponses[n - 1]
        self.numero_reponse = 0
        
        
        # polices de textes à afficher
        fontc = pygame.font.Font(None, 60)
        fontreponse = pygame.font.Font(None, 30)
        font_time = pygame.font.Font(None, 40)
        font_lose = pygame.font.Font(None, 50)
        
        questionn = fontc.render(self.question, True, (0, 0, 0))
        reponseA = fontreponse.render(self.reponsess[0], True, (0, 0, 0))
        reponseB = fontreponse.render(self.reponsess[1], True, (0, 0, 0))
        reponseC = fontreponse.render(self.reponsess[2], True, (0, 0, 0))
        reponseD = fontreponse.render(self.reponsess[3], True, (0, 0, 0))
        
        
        start_time = pygame.time.get_ticks()

        while self.running :
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            remaining_time = max(10 - elapsed_time, 0)
            

            if not self.Loose : 
                self.screen.blit(self.image, (255, 0))
                self.screen.blit(questionn, (300, 50))
                self.screen.blit(reponseA, (350, 500))
                self.screen.blit(reponseB, (750, 500))
                self.screen.blit(reponseC, (350, 600))
                self.screen.blit(reponseD, (750, 600))

                # checkboxs
                pygame.draw.rect(self.screen, (0, 0, 0), self.case_A, 2)
                pygame.draw.rect(self.screen, (0, 0, 0), self.case_B, 2)
                pygame.draw.rect(self.screen, (0, 0, 0), self.case_C, 2)
                pygame.draw.rect(self.screen, (0, 0, 0), self.case_D, 2)

                # si on clique sur une des cases

                if self.checked_A:
                    self.reponse_joueur = self.reponsess[0]
                    pygame.draw.line(self.screen, (0, 0, 0), (self.case_A.left + 4, self.case_A.centery),
                         (self.case_A.centerx, self.case_A.bottom - 4), 2)
                    pygame.draw.line(self.screen, (0, 0, 0), (self.case_A.centerx, self.case_A.bottom - 4),
                                    (self.case_A.right - 4, self.case_A.top + 4), 2)
                    if self.verification(self.question,self.reponse_joueur):
                        self.Win = True
                    else : self.Perdu = True

                if self.checked_B:
                    self.reponse_joueur = self.reponsess[1]
                    pygame.draw.line(self.screen, (0, 0, 0), (self.case_B.left + 4, self.case_B.centery),
                         (self.case_B.centerx, self.case_B.bottom - 4), 2)
                    pygame.draw.line(self.screen, (0, 0, 0), (self.case_B.centerx, self.case_B.bottom - 4),
                                    (self.case_B.right - 4, self.case_B.top + 4), 2)
                    if self.verification(self.question,self.reponse_joueur):
                        self.Win = True
                    else : self.Perdu = True
                
                if self.checked_C:
                    self.reponse_joueur = self.reponsess[2]
                    pygame.draw.line(self.screen, (0, 0, 0), (self.case_C.left + 4, self.case_C.centery),
                         (self.case_C.centerx, self.case_C.bottom - 4), 2)
                    pygame.draw.line(self.screen, (0, 0, 0), (self.case_C.centerx, self.case_C.bottom - 4),
                                    (self.case_C.right - 4, self.case_C.top + 4), 2)
                    if self.verification(self.question,self.reponse_joueur):
                        self.Win = True
                    else : self.Perdu = True
                    
                if self.checked_D:
                    self.reponse_joueur = self.reponsess[3]
                    pygame.draw.line(self.screen, (0, 0, 0), (self.case_D.left + 4, self.case_D.centery),
                         (self.case_D.centerx, self.case_D.bottom - 4), 2)
                    pygame.draw.line(self.screen, (0, 0, 0), (self.case_D.centerx, self.case_D.bottom - 4),
                                    (self.case_D.right - 4, self.case_D.top + 4), 2)
                    if self.verification(self.question,self.reponse_joueur):
                        self.Win = True
                    else : self.Perdu = True

                ## pour les cases, à gerer plus tard si temps

            
                timer_text = font_time.render(f"Temps restant : {remaining_time}", True, (255, 0, 0))
                self.screen.blit(timer_text, (50, 50))
            
            pygame.display.update()
            
            if remaining_time == 0 or self.Perdu:
                lose_text = font_lose.render("Vous avez perdu.", True, (255, 0, 0))
                self.screen.blit(lose_text, (250, 400))
                pygame.display.update()
                time.sleep(3)
                pygame.display.update()
                self.Loose = True
                self.running = False

            ## il faudrait concevoir le fait que les questions peuvent être clicables afin de récupérer la réponse du joueur afin de la comparer à la bonne réponse 
                
            if self.Win:
                win_text = font_lose.render("Vous avez la bonne réponse.",True,(0,255,0))
                self.screen.blit(win_text,(250,400))
                pygame.display.update()
                time.sleep(3)
                pygame.display.update()
                self.Loose = True
                self.running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.case_A.collidepoint(event.pos):
                        self.checked_A = not self.checked_A
                    if self.case_B.collidepoint(event.pos):
                        self.checked_B = not self.checked_B
                    if self.case_C.collidepoint(event.pos):
                        self.checked_C = not self.checked_C
                    if self.case_D.collidepoint(event.pos):
                        self.checked_D = not self.checked_D



dico = """{
    'question 1 : Qui est le singe' : ['réponse A : Tu es fous','réponse B : Tu es fouuu','réponse C : Tu es picece','réponse D : rhgreg','bonne réponse : Tu es fous'],
    'question 2 : Quelle est la couleur du ciel ?' : ['réponse A : Rouge','réponse B : Bleu','réponse C : Vert','réponse D : Noir','bonne réponse : Bleu']
}"""

#print(Enigme(dico).verification('question 2 : Quelle est la couleur du ciel ?','réponse A : Rouge'))