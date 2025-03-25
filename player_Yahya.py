
import pygame

class Player(pygame.sprite.Sprite): 
    def __init__(self,pos_x,pos_y,screen):
        super().__init__()  # Initialisation du sprite
        self.x = pos_x
        self.y = pos_y
        self.speed = 2
        self.speed_run = 3.5
        self.screen = screen
        self.health_value = 100
        self.mana_value = 0
        self.endurance_value = 100

        #On stocke ici les mouvement du personnage selon s'il va en haut, en bas, a droite ou a gauche
        self.down  =  [pygame.image.load(f"animation/walk/walk1/down{i}.png") for i in range(1, 6)]
        self.up    =  [pygame.image.load(f"animation/walk/walk2/up{j}.png") for j in range(1, 6)]
        self.right =  [pygame.image.load(f"animation/walk/walk3/right{j}.png") for j in range(1, 6)]
        self.left  =  [pygame.image.load(f"animation/walk/walk4/left{j}.png") for j in range(1, 6)]
        
        #UI
        self.profile = pygame.image.load("UI/profil.png")
        self.health = [pygame.image.load(f"UI/vie/health{j}.png") for j in range(1, 8)]
        self.mana = [pygame.image.load(f"UI/mana/mana{j}.png") for j in range(1, 7)]
        self.endurance = [pygame.image.load(f"UI/endurance/endurance{j}.png") for j in range(1, 7)]

        #Current 
        self.current_health = self.health[0]
        self.current_mana = self.mana[5]
        self.current_endurance = self.endurance[0]

        #On stocke ici les mouvements de l'idle 
        self.idle_down_mouv = [pygame.image.load(f"animation/idle/idle1/down{j}.png") for j in range(1, 4)]
        self.idle_up_mouv = [pygame.image.load(f"animation/idle/idle2/up{j}.png") for j in range(1, 4)]
        self.idle_right_mouv = [pygame.image.load(f"animation/idle/idle3/right{j}.png") for j in range(1, 4)]
        self.idle_left_mouv = [pygame.image.load(f"animation/idle/idle4/left{j}.png") for j in range(1, 4)]

        self.attack_right_mouv = [pygame.image.load(f"animation/attack/attack1/right{j}.png") for j in range(1, 5)]

        #Index que l'on utlise pour l'animation
        self.current_sprite = 0
        #On prend comme image de base idle1
        self.image = pygame.image.load("animation/idle/idle1/down1.png")
        #On récupère le rectangle de l'image
        self.rect = self.image.get_rect()

        # Variable qui stocke la dernière direction du personnage, par défaut on la met à down
        self.last_direction = "down"
        print(self.health_value)
    
    
    def animation(self,liste_mouv,speed):
        self.current_sprite += speed
        if self.current_sprite >=len(liste_mouv):
            self.current_sprite = 0
        self.image = liste_mouv[int(self.current_sprite)]

    

    def move_left(self):
        self.rect.x -=self.speed
        self.animation(self.left,0.15)
        self.last_direction = "left"
        
    
    def move_right(self):
        self.rect.x +=self.speed
        self.animation(self.right,0.15)
        self.last_direction = "right"
        self.endurance_value-=0.125
        
    
    def move_up(self):
        self.rect.y -=self.speed
        self.animation(self.up,0.15)
        self.last_direction = "up"

    def move_down(self):
        self.rect.y +=self.speed
        self.animation(self.down,0.15)
        self.last_direction = "down"

    #Méthodes pour le sprint
    def run_left(self):
        self.rect.x -=self.speed_run
        self.animation(self.left,0.3)
    
    def run_right(self):
        self.rect.x +=self.speed_run
        self.animation(self.right,0.3)
    
    def run_up(self):
        self.rect.y -=self.speed_run
        self.animation(self.up,0.3)

    def run_down(self):
        self.rect.y +=self.speed_run
        self.animation(self.down,0.3)

    #méthodes pour gérer l'idle
    def idle_up(self):
        self.animation(self.idle_up_mouv,0.15)
        
    def idle_down(self):
        self.animation(self.idle_down_mouv,0.15)

    def idle_left(self):
        self.animation(self.idle_left_mouv,0.15)

    def idle_right(self):
        self.animation(self.idle_right_mouv,0.15)

    def affiche_ui(self):
        #Gestion affichage de la barre de vie selon la valeur de la vie
        if 0 < self.health_value < 20:
            self.current_health = self.health[5]
        elif 20 < self.health_value < 40:
            self.current_health = self.health[4]
        elif 40 < self.health_value < 60:
            self.current_health = self.health[3]
        elif 60 < self.health_value < 80:
            self.current_health = self.health[2]

        elif 80 < self.health_value < 99:
            self.current_health = self.health[1]
        elif self.health_value == 100:
            self.current_health = self.health[0]
        elif self.health_value == 0:
            self.current_health = self.health[6]

        if self.health_value < 1:
            self.health_value = 0
        elif self.health_value >99:
            self.health_value = 100
        #Gestion affichage de la barre d'endurance selon la valeur de l'endurance
        if 0 < self.endurance_value < 20:
            self.current_endurance = self.endurance[4]
        elif 20 < self.endurance_value < 40:
            self.current_endurance = self.endurance[3]
        elif 40 < self.endurance_value < 60:
            self.current_endurance = self.endurance[2]
        elif 60 < self.endurance_value < 80:
            self.current_endurance = self.endurance[1]
        elif self.endurance_value == 100:
            self.current_endurance = self.endurance[0]
        elif self.endurance_value == 0:
            self.current_endurance = self.endurance[5]

    

        self.screen.blit(self.profile,(15,30))
        self.screen.blit(self.current_health,(100,15))
        self.screen.blit(self.current_mana,(93,65))
        self.screen.blit(self.current_endurance,(10,120))





