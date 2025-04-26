import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self,name,x,y,type,screen):
        super().__init__()
        self.name = name
        self.image = pygame.image.load(f"{type}/{name}/idle/idle1.png")
        self.right_move = [pygame.image.load(f"{type}/{name}/walk/walk1/right{i}.png")for i in range(1,10)]
        self.idle_move = [pygame.image.load(f"{type}/{name}/idle/idle{i}.png")for i in range(1,4)]
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect()
        
        self.font_dialog_box_name = pygame.font.Font("UI/dialog_font.ttf", 20)
        self.font_dialog_box = pygame.font.Font("UI/dialog_font.ttf", 15)

        self.rect.x = x
        self.rect.y = y
        self.hit_box = self.rect.copy().inflate(-30,0)
        self.champ_vision = self.rect.copy().inflate(20,20)

        self.sprite_index = 0
        self.parole = [f"Salutations, je suis {name}.",
                       "Je serais ton guide dans ce monde",
                       "J'ai besoin de ton aide pour sécuriser cette clairière",
                       "Des gobelins on pris possesion de cette terre tu dois les exterminer",
                       "Voila un objet qui te sera utile, bonne chance."]
        self.right = True
        self.dialog_box = pygame.image.load("UI/dialog_box_gris.png")
        self.dialog_box_name = pygame.image.load("UI/dialog_box_nom.png")
        self.portrait = pygame.image.load(f"{type}/{name}/portrait2.png")
        self.screen = screen

        self.CanDialog = False
        self.name_entity = self.font_dialog_box_name.render(self.name,True, (255, 255, 111))
        self.entity_parole = self.font_dialog_box.render(self.parole[3],True, (255, 255, 111))

        self.current_text = ""    # Le texte affiché progressivement
        self.full_text = ""       # Le texte complet à afficher
        self.text_index = 0       # Où on en est dans le texte
        self.last_update_time = pygame.time.get_ticks()  # Pour gérer la vitesse
        self.text_speed = 50      # Millisecondes entre chaque lettre (plus petit = plus rapide)
        self.current_parole_index = 0  # Numéro de la phrase actuelle


    def animation(self,list_mouv,speed):
        self.sprite_index += speed
        if self.sprite_index >=len(list_mouv):
            self.sprite_index = 0
        self.image = list_mouv[int(self.sprite_index)]
        self.image = pygame.transform.scale(self.image,(50,50))

    def droite(self):
        self.rect.x += 1
        self.animation(self.right_move,0.20)
        
    def idle(self):
        self.animation(self.idle_move,0.12)

    def haut(self):
        self.rect.y += 1

    def bas(self):
        self.rect.y -= 1

    def gauche(self):
        self.rect.x -= 1

    def update(self):
        if self.CanDialog:
            self.screen.blit(self.dialog_box,(300,600))
            self.screen.blit(self.portrait,(360,500))
            self.screen.blit(self.dialog_box_name,(350,750))
            self.screen.blit(self.name_entity,(410,770))

            # Animation lettre par lettre
            now = pygame.time.get_ticks()
            if now - self.last_update_time > self.text_speed:
                if self.text_index < len(self.full_text):
                    self.current_text += self.full_text[self.text_index]
                    self.text_index += 1
                    self.last_update_time = now

            text_surface = self.font_dialog_box.render(self.current_text, True, (255, 255, 111))
            self.screen.blit(text_surface, (600, 660))

    def start_dialog(self, index=0):
        self.full_text = self.parole[index]
        self.current_text = ""
        self.text_index = 0
        self.current_parole_index = index
        self.last_update_time = pygame.time.get_ticks()
        
    def next_dialog(self):
        if self.current_parole_index + 1 < len(self.parole):
            self.current_parole_index += 1
            self.start_dialog(self.current_parole_index)
        else:
            self.CanDialog = False  # Plus de texte = fermer la boîte

# On crée ici une classe qui hérite de la classe Entity
class PNJ(Entity):
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
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.collision = False
        pass

    def pattern(self,limx1,limx2,limy1,limy2):
        """
            Crée un pattern de forme rectangulaire de mouvement pour le PNJ
        """
        pass

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

