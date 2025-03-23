
import pygame

class Player: 
    def __init__(self,pos_x,pos_y,screen):
        self.x = pos_x
        self.y = pos_y
        self.speed = 2
        self.speed_run = 3.5
        self.screen = screen
        
        #On stocke ici les mouvement du personnage selon s'il va en haut, en bas, a droite ou a gauche
        self.down  =  [pygame.image.load(f"anim/walk/walk1/walk{i}.png") for i in range(1, 6)]
        self.up    =  [pygame.image.load(f"anim/walk/walk2/up{j}.png") for j in range(1, 6)]
        self.right =  [pygame.image.load(f"anim/walk/walk3/right{j}.png") for j in range(1, 6)]
        self.left  =  [pygame.image.load(f"anim/walk/walk4/left{j}.png") for j in range(1, 6)]
        #On stocke ici les mouvment du sprint
        self.run_down_mouv = [pygame.image.load(f"anim/run/run1/down{j}.png") for j in range(1, 6)]
        self.run_up_mouv = [pygame.image.load(f"anim/run/run2/up{j}.png") for j in range(1, 6)]
        self.run_right_mouv = [pygame.image.load(f"anim/run/run3/right{j}.png") for j in range(1, 4)]
        self.run_left_mouv = [pygame.image.load(f"anim/run/run4/left{j}.png") for j in range(1, 4)]
        #Index que l'on utlise pour l'animation
        self.current_sprite = 0
        self.image = pygame.image.load("anim\idle1.png")
        self.rectangle = self.image.get_rect()


    def affiche(self):
        self.screen.blit(self.image,(self.x,self.y))

    def animation(self,liste_mouv):
        self.current_sprite += 0.15
        if self.current_sprite >=len(liste_mouv):
            self.current_sprite = 0
        self.image = liste_mouv[int(self.current_sprite)]
    
    def move_left(self):
        self.x -=self.speed
        self.animation(self.left)
    
    def move_right(self):
        self.x +=self.speed
        self.animation(self.right)
    
    def move_up(self):
        self.y -=self.speed
        self.animation(self.up)

    def move_down(self):
        self.y +=self.speed
        self.animation(self.down)

    #Méthodes pour le sprint
    def run_left(self):
        self.x -=self.speed_run
        self.animation(self.run_left_mouv)
    
    def run_right(self):
        self.x +=self.speed_run
        self.animation(self.run_right_mouv)
    
    def run_up(self):
        self.y -=self.speed_run
        self.animation(self.run_up_mouv)

    def run_down(self):
        self.y +=self.speed_run
        self.animation(self.run_down_mouv)
        