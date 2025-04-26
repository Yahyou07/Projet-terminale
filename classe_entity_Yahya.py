import pygame

class Entity(pygame.sprite.Sprite):
    """
        Classe Entity qui hérite de la classe Sprite de Pygame
        Attributs:
            name : nom de l'entité
            x : position x de l'entité 
            y : position y de l'entité
            type : type de l'entité (string)
            screen : écran sur lequel l'entité est affichée
        """
    def __init__(self,name,x,y,type,screen):
        super().__init__()
        self.name = name
        self.image = pygame.image.load(f"{type}/{name}/idle/idle1.png")
        self.right_move = [pygame.image.load(f"{type}/{name}/walk/walk1/right{i}.png")for i in range(1,10)]
        self.left_move = [pygame.image.load(f"{type}/{name}/walk/walk2/left{i}.png")for i in range(1,10)]
        self.top_move = [pygame.image.load(f"{type}/{name}/walk/walk3/top{i}.png")for i in range(1,10)]
        self.bottom_move = [pygame.image.load(f"{type}/{name}/walk/walk4/bottom{i}.png")for i in range(1,10)]

        self.idle_move = [pygame.image.load(f"{type}/{name}/idle/idle{i}.png")for i in range(1,4)]
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect()
        
        

        self.rect.x = x
        self.rect.y = y
        self.hit_box = self.rect.copy().inflate(-30,0)
        self.champ_vision = self.rect.copy().inflate(20,20)

        self.sprite_index = 0
        
        self.right = True
        self.screen = screen
       


    def animation(self,list_mouv,speed):
        """
            Animation de l'entité
            Attributs:
                list_mouv : liste des images de l'animation
                speed : vitesse de l'animation
        """
        self.sprite_index += speed
        if self.sprite_index >=len(list_mouv):
            self.sprite_index = 0
        self.image = list_mouv[int(self.sprite_index)]
        self.image = pygame.transform.scale(self.image,(50,50))

    def droite(self):
        """
            Déplacement de l'entité vers la droite
        """
        self.rect.x += 1
        self.animation(self.right_move,0.20)
        
    def idle(self):
        """
            Animation idle de l'entité
        """
        self.animation(self.idle_move,0.12)

    def haut(self):
        """
            Déplacement de l'entité vers le haut
        """
        self.rect.y -= 1
        self.animation(self.top_move,0.20)

    def bas(self):
        """
            Déplacement de l'entité vers le bas
        """
        self.rect.y += 1
        self.animation(self.bottom_move,0.2)

    def gauche(self):
        """
            Déplacement de l'entité vers la gauche
        """
        self.rect.x -= 1
        self.animation(self.left_move,0.2)

    

class PNJ(Entity):
    def __init__(self, name, x, y, type, screen):
        """
        Classe PNJ qui hérite de la classe Entity
        Attributs:
            name : nom du PNJ
            x : position x du PNJ
            y : position y du PNJ
            collision : collision du PNJ (booléen)
            speed : vitesse de déplacement du PNJ
            health_value : vie du PNJ
            attack_value : valeur d'attaque
        """
        super().__init__(name, x, y, type, screen)
        self.dialog_box = pygame.image.load("UI/dialog_box_gris.png")
        self.dialog_box_name = pygame.image.load("UI/dialog_box_nom.png")
        self.portrait = pygame.image.load(f"{type}/{name}/portrait.png")
        
        self.font_dialog_box_name = pygame.font.Font("UI/dialog_font.ttf", 20)
        self.font_dialog_box = pygame.font.Font("UI/dialog_font.ttf", 15)

        self.CanDialog = False
        

        self.current_text = ""    # Le texte affiché progressivement
        self.full_text = ""       # Le texte complet à afficher
        self.text_index = 0       # Où on en est dans le texte
        self.last_update_time = pygame.time.get_ticks()  # Pour gérer la vitesse
        self.text_speed = 30      # Millisecondes entre chaque lettre (plus petit = plus rapide)
        self.current_parole_index = 0  # Numéro de la phrase actuelle
    
        self.parole = [f"Salutations, je suis {name}.",
                       "Je serais ton guide dans ce monde",
                       "J'ai besoin de ton aide pour \n sécuriser  cette clairière",
                       "Des gobelins on pris possesion \n de cette terre tu dois les exterminer",
                       "Suis le chemin et tu les trouvera,\n bonne chance."]
        
        self.name_entity = self.font_dialog_box_name.render(self.name,True, (255, 255, 111))
        self.entity_parole = self.font_dialog_box.render(self.parole[3],True, (255, 255, 111))
        
    def update(self):
        """
            Met à jour l'entité
        """
        if self.CanDialog:
            self.screen.blit(self.dialog_box,(300,600))
            self.screen.blit(self.portrait,(360,500))
            self.screen.blit(self.dialog_box_name,(350,750))
            self.screen.blit(self.name_entity,(410,770))

            now = pygame.time.get_ticks()
            if now - self.last_update_time > self.text_speed:
                if self.text_index < len(self.full_text):
                    self.current_text += self.full_text[self.text_index]
                    self.text_index += 1
                    self.last_update_time = now

            # --------- Affichage avec saut de ligne ---------
            lines = self.current_text.split('\n')  # ← ici
            for i, line in enumerate(lines):
                line_surface = self.font_dialog_box.render(line, True, (255, 255, 111))
                self.screen.blit(line_surface, (580, 660 + i * 30))  # ← 25 px entre chaque ligne


    def start_dialog(self, index=0):
        """
            Démarre le dialogue avec l'entité
            Attributs:
                index : index de la phrase à afficher
        """
        self.full_text = self.parole[index]
        self.current_text = ""
        self.text_index = 0
        self.current_parole_index = index
        self.last_update_time = pygame.time.get_ticks()
        
    def next_dialog(self):
        """
            Passe à la phrase suivante du dialogue
        """
        if self.current_parole_index + 1 < len(self.parole):
            self.current_parole_index += 1
            self.start_dialog(self.current_parole_index)
        else:
            self.CanDialog = False  # Plus de texte = fermer la boîte
            


class Enemy(Entity):
    def __init__(self, name, x, y, type, screen):
        super().__init__(name, x, y, type, screen)

        self.dead_mouve = [pygame.image.load(f"{type}/{name}/dead/dead{i}.png")for i in range(1,7)]
        self.champ_vision_enemy = self.rect.copy().inflate(300, 300)  # Champ de vision agrandi autour de l'ennemi
        self.speed = 1  # Vitesse de déplacement vers le joueur
        self.detected_player = False  # Si le joueur est détecté

        
    def dead(self):
        self.animation(self.dead_mouve,0.12)
    
    def follow_player(self, player):
        """ Fait bouger l'ennemi vers le joueur en diagonale, mais avec anim gauche/droite seulement """
        if self.champ_vision_enemy.colliderect(player.rect):
            self.detected_player = True
        else:
            self.detected_player = False

        if self.detected_player:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery

            if dx != 0:
                self.rect.x += self.speed if dx > 0 else -self.speed
            if dy != 0:
                self.rect.y += self.speed if dy > 0 else -self.speed

            # Maintenant choisir l'animation : droite ou gauche selon dx
            if dx > 0:
                self.animation(self.right_move, 0.2)
            elif dx < 0:
                self.animation(self.left_move, 0.2)

        else:
            self.idle()

    '''
    def follow_player(self, player):
        """ Fait bouger l'ennemi vers le joueur s'il est détecté """
        if self.champ_vision_enemy.colliderect(player.rect):
            self.detected_player = True
        else:
            self.detected_player = False

        if self.detected_player:
            if self.rect.x < player.rect.x:
                self.rect.x += self.speed
                self.animation(self.right_move, 0.2)
            elif self.rect.x > player.rect.x:
                self.rect.x -= self.speed
                self.animation(self.left_move, 0.2)
            if self.rect.y < player.rect.y:
                self.rect.y += self.speed
                self.animation(self.bottom_move, 0.2)
            elif self.rect.y > player.rect.y:
                self.rect.y -= self.speed
                self.animation(self.top_move, 0.2)
        else:
            self.idle()
        '''
    
class Mob(Entity):
    """
        Classe Mob qui hérite de la classe Entity
        Attributs:
            name : nom du mob
            x : position x du mob
            y : position y du mob
            collision : collision du mob (booléen)
            speed : vitesse de déplacement du mob
            health_value : vie du mob
            attack_value : valeur d'attaque du mob
            type : type du mob (string)
    """
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.collision = False
        self.speed = 1
        self.health_value = 10
        self.attack_value = 1
        self.type = "mob"
    
    def follow_player(self, player):
        """
            Fait suivre le joueur au mob.
            Attributs:
                player : le joueur à suivre
        """
        if self.distance(player) < 50:
            while self.rect.x != player.rect.x:
                if self.rect.x < player.rect.x:
                    self.rect.x += self.speed
                elif self.rect.x > player.rect.x:
                    self.rect.x -= self.speed
            while self.rect.y != player.rect.y:
                if self.rect.y < player.rect.y:
                    self.rect.y += self.speed
                elif self.rect.y > player.rect.y:
                    self.rect.y -= self.speed
            if self.distance(player) == 0:
                self.attack_player(player)
    
    def attack_player(self, player):
        """
            Fait attaquer le joueur par le mob lorsque la distance est nulle.
            Attributs:
                player : le joueur à attaquer
        """
        while player.health_value > 0:
            player.health_value -= self.attack_value
            print(f"{self.name} attaque {player.name} !")
            if player.health_value <= 0:
                print(f"{player.name} est mort !")
                break

