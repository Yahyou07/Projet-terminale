
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
        self.font = pygame.font.Font("Items/Minecraft.ttf", 14)  # Police par défaut, taille 20
        self.Regen = False

        self.inventory_image = pygame.image.load("UI/Inventories/inventaire_bag.png")

        
        #self.stack_text = self.font.render("0", True, (255, 255, 255))  # Texte blanc

        # Paramètres de l'inventaire
        self.INV_X = 478  # Position X de l'inventaire
        self.INV_Y = self.screen.get_height()-0.1*self.screen.get_height()  # Position Y de l'inventaire
        self.CELL_SIZE = 50
        self.CELL_SPACING = 25
        self.INV_COLS = 10

        #Liste de la barre d'inventaire
        self.inventory_bar_list = [{} for i in range(10)]
        self.inventory_icons = [pygame.image.load(f"Items/slot.png")for i in range(10)]
        self.stack_text = [self.font.render("", True, (255, 255, 255)) for i in range(10)] 
        
        #Tableaux de l'inventaire :
        # Inventaire étendu (sac) : 6 colonnes × 5 lignes = 30 emplacements
        self.inventory_list = [[{} for _ in range(6)] for _ in range(5)]
        self.inventory_bag_icon = [[pygame.image.load("Items/slot.png") for _ in range(6)] for _ in range(5)]
        self.inventory_bag_stack_text = [[self.font.render("", True, (255, 255, 255)) for _ in range(6)] for _ in range(5)]
        
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

        self.attack_right_mouv = [pygame.image.load(f"animation/attack/attack1/right{j}.png") for j in range(1, 6)]

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
        
        #Attribut pour le dragging and drop
        self.dragging_item = None  # Contiendra un dict comme {"name": ..., "icon": ..., "stack": ...}
        self.dragging_from = None  # ("bar", index) ou ("bag", row, col)
    
    
    def animation(self,liste_mouv,speed):
        self.current_sprite += speed
        if self.current_sprite >=len(liste_mouv):
            self.current_sprite = 0
        self.image = liste_mouv[int(self.current_sprite)]

    #def attack(self, attacking=True):
        #animation d'attaque
        #attaque_speed = 0.3
        

    def move(self, dx, dy, attacking, running=False, ):
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)
        speed = self.speed_run if running else self.speed
        if dx != 0 and dy != 0:
            speed /= math.sqrt(2)  # Normalisation de la vitesse en diagonale

        self.rect.x += dx * speed
        self.rect.y += dy * speed

        # Gestion des animations
        attaque_speed = 0.3
        anim_speed = 0.3 if running else 0.15
        if dx > 0:
            self.animation(self.right, anim_speed)
            self.last_direction = "right"
            print(dx)
        elif dx < 0:
            self.animation(self.left, anim_speed)
            self.last_direction = "left"
        elif dy > 0:
            self.animation(self.down, anim_speed)
            self.last_direction = "down"
        elif dy < 0:
            self.animation(self.up, anim_speed)
            self.last_direction = "up"

        elif attacking == 1:
            self.animation(self.attack_right_mouv, attaque_speed)
            self.last_direction = "right"

        

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

    #def idle_right_attack(self):
        #self.animation(self.attack_right_mouv,0.15)

    def affiche_ui(self):
        foundd = 0
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
        elif self.health_value > 99:
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
        
        x = 485
        for icon in self.inventory_icons:
            self.screen.blit(icon,(x,self.screen.get_height()-0.09*self.screen.get_height()))
            x += 60
        x_stack = 520
        for stack in self.stack_text:
            self.screen.blit(stack,(x_stack,self.screen.get_height()-0.07*self.screen.get_height()))
            x_stack += 60
        # Contour vert pour slots vides de la barre d'inventaire
        
 
    def display_inventory(self):     
                # Affiche l'image de l'inventaire centrée à l'écran
        x = self.screen.get_width() // 2 - self.inventory_image.get_width() // 2 - 50
        y = self.screen.get_height() // 2 - self.inventory_image.get_height() // 2
        self.screen.blit(self.inventory_image, (x, y))  

        # Affichage du contenu de l'inventaire sac (6x5)
        start_x = 595  # Position X de la première cellule
        start_y = 290  # Position Y de la première cellule
        for row in range(5):
            for col in range(6):
                slot_x = start_x + col * (self.CELL_SIZE + self.CELL_SPACING)
                slot_y = start_y + row * (self.CELL_SIZE + self.CELL_SPACING)
                icon = self.inventory_bag_icon[row][col]
                stack = self.inventory_bag_stack_text[row][col]

                self.screen.blit(icon, (slot_x, slot_y))
                self.screen.blit(stack, (slot_x + 25, slot_y + 30))  # Position du texte dans la cellule


       

    
    
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
                
            if 1<elapsed<2:
                self.endurance_value = 39
                
            if 2<elapsed<3:
                self.endurance_value = 59
                
            if 3<elapsed<4:
                self.endurance_value = 79
                
            if elapsed>=5:
                self.endurance_value = 100
                
    
    
    def add_to_inventory(self, sprite):
        
        found = False

        # D'abord on tente dans la barre rapide
        for i in range(len(self.inventory_bar_list)):
            slot = self.inventory_bar_list[i]
            if slot and list(slot.keys())[0] == sprite.name:
                sprite.stack = list(slot.values())[0]
                if sprite.stack < sprite.stack_max:
                    stack_total = sprite.stack + 1
                    self.inventory_bar_list[i] = {sprite.name: stack_total}
                    self.inventory_icons[i] = sprite.icon
                    self.stack_text[i] = self.font.render(str(stack_total), True, (255, 255, 255))
                    found = True
                break

        if not found:
            # On essaye de trouver un slot vide dans la barre 
            for i in range(len(self.inventory_bar_list)):
                slot = self.inventory_bar_list[i]
                if not slot or list(slot.keys())[0] == "rien":
                    sprite.stack = 1
                    self.inventory_bar_list[i] = {sprite.name: sprite.stack}
                    self.inventory_icons[i] = sprite.icon
                    self.stack_text[i] = self.font.render("1", True, (255, 255, 255))
                    return

            # Sinon, stocker dans le sac (grille 6x5)
            for row in range(5):
                for col in range(6):
                    slot = self.inventory_list[row][col]
                    if slot and list(slot.keys())[0] == sprite.name:
                        sprite.stack = list(slot.values())[0]
                        if sprite.stack < sprite.stack_max:
                            stack_total = sprite.stack + 1
                            self.inventory_list[row][col] = {sprite.name: stack_total}
                            self.inventory_bag_icon[row][col] = sprite.icon
                            self.inventory_bag_stack_text[row][col] = self.font.render(str(stack_total), True, (255, 255, 255))
                            return

            for row in range(5):
                for col in range(6):
                    slot = self.inventory_list[row][col]
                    if not slot or list(slot.keys())[0] == "rien":
                        sprite.stack = 1
                        self.inventory_list[row][col] = {sprite.name: sprite.stack}
                        self.inventory_bag_icon[row][col] = sprite.icon
                        self.inventory_bag_stack_text[row][col] = self.font.render("1", True, (255, 255, 255))
                        return

        
    def drag_and_drop_inventory(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button ==1:
                print("bonjour")





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