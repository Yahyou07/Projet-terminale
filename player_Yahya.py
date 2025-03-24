
import pygame

class Player(pygame.sprite.Sprite): 
    def __init__(self,pos_x,pos_y,screen):
        super().__init__()  # Initialisation du sprite
        self.x = pos_x
        self.y = pos_y
        self.speed = 2
        self.speed_run = 3.5
        self.screen = screen
        self.health = 100
        self.mana = 0
        self.endurance = 100

        #On stocke ici les mouvement du personnage selon s'il va en haut, en bas, a droite ou a gauche
        self.down  =  [pygame.image.load(f"animation/walk/walk1/down{i}.png") for i in range(1, 6)]
        self.up    =  [pygame.image.load(f"animation/walk/walk2/up{j}.png") for j in range(1, 6)]
        self.right =  [pygame.image.load(f"animation/walk/walk3/right{j}.png") for j in range(1, 6)]
        self.left  =  [pygame.image.load(f"animation/walk/walk4/left{j}.png") for j in range(1, 6)]
        

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

    