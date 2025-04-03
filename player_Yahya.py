
import pygame
import math
import time
class Player(pygame.sprite.Sprite): 
    def __init__(self,pos_x,pos_y,screen):
        super().__init__()  # Initialisation du sprite
        
        self.speed = 3
        self.speed_run = 4.5
        self.screen = screen
        self.health_value = 100
        self.mana_value = 0
        self.endurance_value = 100
        
        self.Regen = False

                # Paramètres de l'inventaire
        self.INV_X = 478  # Position X de l'inventaire
        self.INV_Y = self.screen.get_height()-0.1*self.screen.get_height()  # Position Y de l'inventaire
        self.CELL_SIZE = 50
        self.CELL_SPACING = 10
        self.INV_COLS = 10


        self.inventory_bar_list = [{} for i in range(10)]
        self.inventory_slots = [pygame.Rect(self.INV_X + i * (self.CELL_SIZE + self.CELL_SPACING), self.INV_Y, self.CELL_SIZE, self.CELL_SIZE) for i in range(self.INV_COLS)]
        self.inventory_icons = [pygame.image.load(f"Items\slot.png")for i in range(10)]
        
        self.inventory_index = 0

        #On stocke ici les mouvement du personnage selon s'il marche en haut, en bas, a droite ou a gauche
        self.down  =  [pygame.image.load(f"animation/walk/walk1/down{i}.png") for i in range(1, 6)]
        self.up    =  [pygame.image.load(f"animation/walk/walk2/up{j}.png") for j in range(1, 6)]
        self.right =  [pygame.image.load(f"animation/walk/walk3/right{j}.png") for j in range(1, 6)]
        self.left  =  [pygame.image.load(f"animation/walk/walk4/left{j}.png") for j in range(1, 6)]
        
        #UI
        self.profile = pygame.image.load("UI/profil.png")
        self.health = [pygame.image.load(f"UI/vie/health{j}.png") for j in range(1, 8)]
        self.mana = [pygame.image.load(f"UI/mana/mana{j}.png") for j in range(1, 7)]
        self.endurance = [pygame.image.load(f"UI/endurance/endurance{j}.png") for j in range(1, 7)]
        self.inventory_bar = pygame.image.load("UI/Inventories/barre_outils.png")
        #Current 
        self.current_health = self.health[0]
        self.current_mana = self.mana[5]
        self.current_endurance = self.endurance[0]

        #On stocke ici les mouvements de l'idle 
        self.idle_down_mouv = [pygame.image.load(f"animation/idle/idle1/down{j}.png") for j in range(1, 5)]
        self.idle_up_mouv = [pygame.image.load(f"animation/idle/idle2/up{j}.png") for j in range(1, 5)]
        self.idle_right_mouv = [pygame.image.load(f"animation/idle/idle3/right{j}.png") for j in range(1, 5)]
        self.idle_left_mouv = [pygame.image.load(f"animation/idle/idle4/left{j}.png") for j in range(1, 5)]

        self.attack_right_mouv = [pygame.image.load(f"animation/attack/attack1/right{j}.png") for j in range(1, 5)]

        #Index que l'on utlise pour l'animation
        self.current_sprite = 0
        #On prend comme image de base idle1
        self.image = pygame.image.load("animation/idle/idle1/down1.png")
        #On récupère le rectangle de l'image
        self.rect = self.image.get_rect()
        self.rect.width = 40  # Ajuste la largeur
        self.rect.height = 40  # Ajuste la hauteur
        self.rect.center = (pos_x, pos_y)  # Centre le rectangle
        self.rect.x = pos_x
        self.rect.y = pos_y
        # Variable qui stocke la dernière direction du personnage, par défaut on la met à down
        self.last_direction = "down"
        print(self.health_value)
    
    
    def animation(self,liste_mouv,speed):
        self.current_sprite += speed
        if self.current_sprite >=len(liste_mouv):
            self.current_sprite = 0
        self.image = liste_mouv[int(self.current_sprite)]

    

    def move(self, dx, dy, running=False):
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)
        speed = self.speed_run if running else self.speed
        if dx != 0 and dy != 0:
            speed /= math.sqrt(2)  # Normalisation de la vitesse en diagonale

        self.rect.x += dx * speed
        self.rect.y += dy * speed

        # Gestion des animations
        anim_speed = 0.3 if running else 0.15
        if dx > 0:
            self.animation(self.right, anim_speed)
            self.last_direction = "right"
        elif dx < 0:
            self.animation(self.left, anim_speed)
            self.last_direction = "left"
        elif dy > 0:
            self.animation(self.down, anim_speed)
            self.last_direction = "down"
        elif dy < 0:
            self.animation(self.up, anim_speed)
            self.last_direction = "up"

        # Réduction de l'endurance si le joueur sprinte
        if running:
            self.endurance_value -= 0.25

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

      
    
        #Affichage des différents UI de vie, de mana, d'endurance et le profil
        self.screen.blit(self.profile,(25,30))
        self.screen.blit(self.current_health,(110,15))
        self.screen.blit(self.current_mana,(103,65))
        self.screen.blit(self.current_endurance,(20,120))
        self.screen.blit(self.inventory_bar,(450,self.screen.get_height()-0.15*self.screen.get_height()))
        
        x = 490
        for icon in self.inventory_icons:
            self.screen.blit(icon,(x,820))
            x += 60
      
            
    
    
    def regeneration_endurance(self,keys):
        if self.endurance_value == 0:
            self.Regen = True
        if self.endurance_value == 100:
            self.Regen = False
            self.start_time = None
        
        if self.Regen and self.endurance_value < 100 and not keys[pygame.K_r]:
            if self.start_time is None:  # On initialise une seule fois
                self.start_time = time.time()
            elapsed = time.time() - self.start_time
            if 0<elapsed<1:
                self.endurance_value = 20
                print("on entre dans la première condition")
                print(self.endurance_value)
                print(elapsed)
            if 1<elapsed<2:
                self.endurance_value = 39
                print("on entre dans la 2 eme condition")
                print(self.endurance_value)
                print(elapsed)
            if 2<elapsed<3:
                self.endurance_value = 59
                print("on entre dans la 3 eme condition")
                print(self.endurance_value)
                print(elapsed)
            if 3<elapsed<4:
                self.endurance_value = 79
                print("on entre dans la 4 eme condition")
                print(self.endurance_value)
                print(elapsed)
            if elapsed>=5:
                self.endurance_value = 100
                print("on entre dans la derniere condition")
                print(self.endurance_value)
                print(elapsed)
    
    
    def add_to_inventory(self, sprite, curent_quantity):
        # Vérifier si l'objet est déjà présent dans l'inventaire
        found = False  

        # Parcourir l'inventaire pour voir si l'objet existe déjà
        for i in range(len(self.inventory_bar_list)):
            slot = self.inventory_bar_list[i]  # Récupérer l'emplacement actuel de l'inventaire
            
            if slot and list(slot.keys())[0] == sprite.name:  # Si l'objet est déjà présent
                curent_quantity = list(slot.values())[0]  # Récupérer la quantité actuelle
                
                if curent_quantity < sprite.stack_max:  # Si la pile n'a pas atteint sa limite
                    self.inventory_bar_list[i] = {sprite.name: curent_quantity + 1}  # Ajouter 1 à la pile
                    self.inventory_icons[i] = sprite.icon
                    found = True  # Indiquer que l'objet a été ajouté
                break  # Sortir de la boucle car l'objet a été traité

        # Si l'objet n'a pas été trouvé ou toutes les piles sont pleines, on cherche un emplacement vide
        if not found:
            # Rechercher un slot vide dans l'inventaire
            for i in range(len(self.inventory_bar_list)):
                slot = self.inventory_bar_list[i]  # On récupère l'emplacement actuel
                
                if not slot or list(slot.keys())[0] == "rien":  # Si l'emplacement est vide ou inutilisé
                    self.inventory_bar_list[i] = {sprite.name: 1}  # On crée une nouvelle pile avec 1 objet
                    self.inventory_icons[i] = sprite.icon
                    break  # On sort de la boucle après avoir placé l'objet

    





##################################################################################

#fonctions données par GPT
    '''
    def add_to_inventory(self, item):
        item_name = item.name  # Nom de l'item (ex: "apple" ou "fish")

        for i in range(len(self.inventory_bar_list)):
            if isinstance(self.inventory_bar_list[i], dict) and self.inventory_bar_list[i]["name"] == item_name:
                # Si l'item existe déjà dans l'inventaire et n'a pas atteint sa limite de stack
                if self.inventory_bar_list[i]["quantity"] < item.items[item_name]["stack_max"]:
                    self.inventory_bar_list[i]["quantity"] += 1
                    print(f"Ajout de {item_name} (x{self.inventory_bar_list[i]['quantity']}) à l'emplacement {i}")
                    return

        # Sinon, trouve un emplacement vide et ajoute l'item
        for i in range(len(self.inventory_bar_list)):
            if self.inventory_bar_list[i] == 0:  # Slot vide
                self.inventory_bar_list[i] = {"name": item_name, "quantity": 1}
                print(f"Nouveau {item_name} ajouté à l'inventaire (slot {i})")
                return
    '''

    '''
    def regeneration_endurance(self, keys):
        if self.endurance_value == 0:
            self.Regen = True
        if self.endurance_value == 100:
            self.Regen = False
            self.regen_start_time = None  # Réinitialisation du chrono
        
        if self.Regen and self.endurance_value < 100 and not keys[pygame.K_r]:
            if self.regen_start_time is None:
                self.regen_start_time = time.time()
            
            elapsed = time.time() - self.regen_start_time
            regen_duration = 70  # Durée totale de la régénération en secondes
            regen_rate = 100 / regen_duration  # Points d'endurance récupérés par seconde
            
            new_value = min(100, self.endurance_value + int(elapsed * regen_rate))
            
            if new_value > self.endurance_value:
                self.endurance_value = new_value
                print(f"Endurance: {self.endurance_value}")
            
            if self.endurance_value == 100:
                self.regen_start_time = None  # Arrêt de la régénération'
    
    '''