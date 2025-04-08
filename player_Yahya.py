
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

        # Chargement des images de l'inventaire
        self.inventory_image = pygame.image.load("UI/Inventories/inventaire_bag.png")
        self.inventory_amour = pygame.image.load("UI/Inventories/inventaire_armure final.png")
        
        self.button_armour  = pygame.image.load("UI/Inventories/armour.png")
        self.rect_button_armour = self.button_armour.get_rect()
        self.rect_button_armour.x = 1045
        self.rect_button_armour.y = 408

        self.button_bag  = pygame.image.load("UI/Inventories/bag.png")
        self.rect_button_bag = self.button_bag.get_rect()
        self.rect_button_bag.x = 1045
        self.rect_button_bag.y = 315
        # Booléen pour gérer l'affichage du sac ou de l'inventaire de l'armure
        self.OnBag = True
        self.OnArmour = False

        #self.stack_text = self.font.render("0", True, (255, 255, 255))  # Texte blanc

        # Paramètres de l'inventaire
        self.INV_X = 478  # Position X de l'inventaire
        self.INV_Y = self.screen.get_height()-0.1*self.screen.get_height()  # Position Y de l'inventaire
        self.CELL_SIZE = 50
        self.CELL_SPACING = 23
        self.INV_COLS = 10

        #Liste de la barre d'inventaire
        self.inventory_bar_list = [{} for i in range(10)]
        self.inventory_icons = [pygame.image.load(f"Items/slot.png")for i in range(10)]
        self.stack_text = [self.font.render("", True, (255, 255, 255)) for i in range(10)] 
        
        #Liste qui stoke les slot de l'inventaire de l'armure
        self.armour_list = [{} for i in range(10)]

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

        self.dragging_item = None  # L'objet en cours de glisser-déposer
        self.drag_start_pos = None  # Position de départ de l'objet glissé
    
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
        
        
    def is_mouse_on_slot(self, x, y, width, height):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return x <= mouse_x <= x + width and y <= mouse_y <= y + height
    
    def display_inventory(self):
        
        if self.OnBag:
            # Affichage de l'image de l'inventaire
            x = self.screen.get_width() // 2 - self.inventory_image.get_width() // 2 - 50
            y = self.screen.get_height() // 2 - self.inventory_image.get_height() // 2
            self.screen.blit(self.inventory_image, (x, y))

            start_x = 595  # Position X de la première cellule
            start_y = 290  # Position Y de la première cellule
            for row in range(5):  # 5 lignes
                for col in range(6):  # 6 colonnes
                    slot_x = start_x + col * (self.CELL_SIZE + self.CELL_SPACING)-10
                    slot_y = start_y + row * (self.CELL_SIZE + self.CELL_SPACING)-5
                    icon = self.inventory_bag_icon[row][col]
                    stack = self.inventory_bag_stack_text[row][col]

                    # Si l'objet est glissé sur ce slot, afficher un contour
                    if self.is_mouse_on_slot(slot_x, slot_y, self.CELL_SIZE, self.CELL_SIZE):
                        pygame.draw.rect(self.screen, (0, 255, 0), (slot_x, slot_y, self.CELL_SIZE, self.CELL_SIZE), 3)

                    self.screen.blit(icon, (slot_x, slot_y))
                    self.screen.blit(stack, (slot_x + 25, slot_y + 30))  # Position du texte dans la cellule

            # Si un objet est en cours de glisser-déposer, afficher l'icône à la position de la souris
            if self.dragging_item and 'icon' in self.dragging_item:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Afficher l'icône de l'item au-dessus de la souris
                self.screen.blit(self.dragging_item['icon'], (mouse_x - self.CELL_SIZE // 2, mouse_y - self.CELL_SIZE // 2))

        if self.OnArmour:
            # Affichage de l'image de l'inventaire
            x_armour = self.screen.get_width() // 2 - self.inventory_amour.get_width() // 2 - 50
            y_armour = self.screen.get_height() // 2 - self.inventory_amour.get_height() // 2
            self.screen.blit(self.inventory_amour, (x_armour, y_armour))


        self.screen.blit(self.button_armour,(1045,408))
        
        self.screen.blit(self.button_bag,(1045,315))

    


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

        # Tenter d'empiler dans la barre d'inventaire
        for i in range(len(self.inventory_bar_list)):
            slot = self.inventory_bar_list[i]
            if slot and slot.get("name") == sprite.name:
                current_qty = slot["quantity"]
                if current_qty < sprite.stack_max:
                    stack_total = min(current_qty + 1, sprite.stack_max)
                    self.inventory_bar_list[i] = {'name': sprite.name,'object':sprite ,'quantity': stack_total}
                    self.inventory_icons[i] = sprite.icon
                    self.stack_text[i] = self.font.render(str(stack_total), True, (255, 255, 255))
                    found = True
                break

        if not found:
            # Chercher un slot vide dans la barre
            for i in range(len(self.inventory_bar_list)):
                slot = self.inventory_bar_list[i]
                if not slot or slot.get("name") == "rien":
                    self.inventory_bar_list[i] = {'name': sprite.name,'object':sprite , 'quantity': 1}
                    self.inventory_icons[i] = sprite.icon
                    self.stack_text[i] = self.font.render("1", True, (255, 255, 255))
                    return

            # Tenter d'empiler dans le sac (6x5)
            for row in range(5):
                for col in range(6):
                    slot = self.inventory_list[row][col]
                    if slot and slot.get("name") == sprite.name:
                        current_qty = slot["quantity"]
                        if current_qty < sprite.stack_max:
                            stack_total = min(current_qty + 1, sprite.stack_max)
                            self.inventory_list[row][col] = {'name': sprite.name,'object':sprite , 'quantity': stack_total}
                            self.inventory_bag_icon[row][col] = sprite.icon
                            self.inventory_bag_stack_text[row][col] = self.font.render(str(stack_total), True, (255, 255, 255))
                            return

            # Sinon, chercher un slot vide dans le sac
            for row in range(5):
                for col in range(6):
                    slot = self.inventory_list[row][col]
                    if not slot or slot.get("name") == "rien":
                        self.inventory_list[row][col] = {'name': sprite.name,'object':sprite , 'quantity': 1}
                        self.inventory_bag_icon[row][col] = sprite.icon
                        self.inventory_bag_stack_text[row][col] = self.font.render("1", True, (255, 255, 255))
                        return


    def handle_mouse_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Clic sur barre d'inventaire
            for i in range(10):
                if self.is_mouse_on_slot(485 + i * 60, self.screen.get_height() - 90, 50, 50):
                    if self.inventory_bar_list[i]:
                        self.dragging_item = self.inventory_bar_list[i]
                        self.dragging_item['icon'] = self.inventory_icons[i]
                        self.drag_start_pos = ("bar", i)
                        self.inventory_bar_list[i] = {}
                        self.inventory_icons[i] = pygame.image.load("Items/slot.png")
                        self.stack_text[i] = pygame.image.load("Items/slot.png")

            # Clic sur sac
            for row in range(5):
                for col in range(6):
                    if self.is_mouse_on_slot(595 + col * (self.CELL_SIZE + self.CELL_SPACING),
                                            290 + row * (self.CELL_SIZE + self.CELL_SPACING),
                                            self.CELL_SIZE, self.CELL_SIZE):
                        if self.inventory_list[row][col]:
                            self.dragging_item = self.inventory_list[row][col]
                            self.dragging_item['icon'] = self.inventory_bag_icon[row][col]
                            self.drag_start_pos = ("bag", row, col)
                            self.inventory_list[row][col] = {}
                            self.inventory_bag_icon[row][col] = pygame.image.load("Items/slot.png")
                            self.inventory_bag_stack_text[row][col] = pygame.image.load("Items/slot.png")

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Déposer dans barre
            for i in range(10):
                if self.is_mouse_on_slot(485 + i * 60, self.screen.get_height() - 90, 50, 50):
                    if self.dragging_item:
                        slot = self.inventory_bar_list[i]
                        if slot and slot['name'] == self.dragging_item['name']:
                            total = slot['quantity'] + self.dragging_item['quantity']
                            stack_max = slot['object'].stack_max
                            if total <= stack_max:
                                slot['quantity'] = total
                                self.stack_text[i] = self.font.render(str(total), True, (255, 255, 255))
                                self.dragging_item = None
                                self.drag_start_pos = None
                                return
                        # Sinon échange
                        if slot:
                            temp, temp_icon, temp_text = slot, self.inventory_icons[i], self.stack_text[i]
                            origin = self.drag_start_pos
                            if origin[0] == "bar":
                                self.inventory_bar_list[origin[1]] = temp
                                self.inventory_icons[origin[1]] = temp_icon
                                self.stack_text[origin[1]] = temp_text
                            else:
                                self.inventory_list[origin[1]][origin[2]] = temp
                                self.inventory_bag_icon[origin[1]][origin[2]] = temp_icon
                                self.inventory_bag_stack_text[origin[1]][origin[2]] = temp_text

                        self.inventory_bar_list[i] = self.dragging_item
                        self.inventory_icons[i] = self.dragging_item['icon']
                        self.stack_text[i] = self.font.render(str(self.dragging_item['quantity']), True, (255, 255, 255))
                        self.dragging_item = None
                        self.drag_start_pos = None
                        break

            # Déposer dans sac
            for row in range(5):
                for col in range(6):
                    if self.is_mouse_on_slot(595 + col * (self.CELL_SIZE + self.CELL_SPACING),
                                            290 + row * (self.CELL_SIZE + self.CELL_SPACING),
                                            self.CELL_SIZE, self.CELL_SIZE):
                        if self.dragging_item:
                            slot = self.inventory_list[row][col]
                            if slot and slot['name'] == self.dragging_item['name']:
                                total = slot['quantity'] + self.dragging_item['quantity']
                                stack_max = slot['object'].stack_max
                                if total <= stack_max:
                                    slot['quantity'] = total
                                    self.inventory_bag_stack_text[row][col] = self.font.render(str(total), True, (255, 255, 255))
                                    self.dragging_item = None
                                    self.drag_start_pos = None
                                    return
                            # Sinon on échange
                            if slot:
                                temp, temp_icon, temp_text = slot, self.inventory_bag_icon[row][col], self.inventory_bag_stack_text[row][col]
                                origin = self.drag_start_pos
                                if origin[0] == "bar":
                                    self.inventory_bar_list[origin[1]] = temp
                                    self.inventory_icons[origin[1]] = temp_icon
                                    self.stack_text[origin[1]] = temp_text
                                else:
                                    self.inventory_list[origin[1]][origin[2]] = temp
                                    self.inventory_bag_icon[origin[1]][origin[2]] = temp_icon
                                    self.inventory_bag_stack_text[origin[1]][origin[2]] = temp_text

                            self.inventory_list[row][col] = self.dragging_item
                            self.inventory_bag_icon[row][col] = self.dragging_item['icon']
                            self.inventory_bag_stack_text[row][col] = self.font.render(str(self.dragging_item['quantity']), True, (255, 255, 255))
                            self.dragging_item = None
                            self.drag_start_pos = None
                            break
            # Si on a relâché en dehors de tout slot, on remet l'objet à sa place d'origine
            if self.dragging_item and self.drag_start_pos:
                origin = self.drag_start_pos
                if origin[0] == "bar":
                    self.inventory_bar_list[origin[1]] = self.dragging_item
                    self.inventory_icons[origin[1]] = self.dragging_item['icon']
                    self.stack_text[origin[1]] = self.font.render(str(self.dragging_item['quantity']), True, (255, 255, 255))
                elif origin[0] == "bag":
                    self.inventory_list[origin[1]][origin[2]] = self.dragging_item
                    self.inventory_bag_icon[origin[1]][origin[2]] = self.dragging_item['icon']
                    self.inventory_bag_stack_text[origin[1]][origin[2]] = self.font.render(str(self.dragging_item['quantity']), True, (255, 255, 255))
                self.dragging_item = None
                self.drag_start_pos = None
    

    '''
    def handle_mouse_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Vérifier si la souris est sur un slot de la barre d'inventaire
            for i in range(10):
                if self.is_mouse_on_slot(485 + i * 60, self.screen.get_height() - 90, 50, 50):
                    if self.inventory_bar_list[i]:
                        self.dragging_item = self.inventory_bar_list[i]
                        self.dragging_item['icon'] = self.inventory_icons[i]
                        self.drag_start_pos = ("bar", i)
                        self.inventory_bar_list[i] = {}
                        self.inventory_icons[i] = pygame.image.load(f"Items/slot.png")
                        self.stack_text[i] = pygame.image.load(f"Items/slot.png")

            # Vérifier si la souris est sur un slot de l'inventaire 6x5
            for row in range(5):
                for col in range(6):
                    if self.is_mouse_on_slot(595 + col * (self.CELL_SIZE + self.CELL_SPACING), 290 + row * (self.CELL_SIZE + self.CELL_SPACING), self.CELL_SIZE, self.CELL_SIZE):
                        if self.inventory_list[row][col]:
                            self.dragging_item = self.inventory_list[row][col]
                            self.dragging_item['icon'] = self.inventory_bag_icon[row][col]
                            self.drag_start_pos = ("bag", row, col)
                            self.inventory_list[row][col] = {}
                            self.inventory_bag_icon[row][col] = pygame.image.load("Items/slot.png")
                            self.inventory_bag_stack_text[row][col] = pygame.image.load("Items/slot.png")

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Déposer l'objet dans la barre d'outils
            for i in range(10):
                if self.is_mouse_on_slot(485 + i * 60, self.screen.get_height() - 90, 50, 50):
                    if self.dragging_item:
                        # échange
                        if self.inventory_bar_list[i]:
                            temp = self.inventory_bar_list[i]
                            temp_icon = self.inventory_icons[i]
                            temp_text = self.stack_text[i]
                            origin = self.drag_start_pos
                            if origin[0] == "bar":
                                self.inventory_bar_list[origin[1]] = temp
                                self.inventory_icons[origin[1]] = temp_icon
                                self.stack_text[origin[1]] = temp_text
                            elif origin[0] == "bag":
                                self.inventory_list[origin[1]][origin[2]] = temp
                                self.inventory_bag_icon[origin[1]][origin[2]] = temp_icon
                                self.inventory_bag_stack_text[origin[1]][origin[2]] = temp_text
                        self.inventory_bar_list[i] = self.dragging_item
                        self.inventory_icons[i] = self.dragging_item['icon']
                        self.stack_text[i] = self.font.render(str(self.dragging_item['quantity']), True, (255, 255, 255))
                        self.dragging_item = None
                        self.drag_start_pos = None
                        break

            # Déposer dans l'inventaire 6x5
            for row in range(5):
                for col in range(6):
                    if self.is_mouse_on_slot(595 + col * (self.CELL_SIZE + self.CELL_SPACING), 290 + row * (self.CELL_SIZE + self.CELL_SPACING), self.CELL_SIZE, self.CELL_SIZE):
                        if self.dragging_item:
                            # échange
                            if self.inventory_list[row][col]:
                                temp = self.inventory_list[row][col]
                                temp_icon = self.inventory_bag_icon[row][col]
                                temp_text = self.inventory_bag_stack_text[row][col]
                                origin = self.drag_start_pos
                                if origin[0] == "bar":
                                    self.inventory_bar_list[origin[1]] = temp
                                    self.inventory_icons[origin[1]] = temp_icon
                                    self.stack_text[origin[1]] = temp_text
                                elif origin[0] == "bag":
                                    self.inventory_list[origin[1]][origin[2]] = temp
                                    self.inventory_bag_icon[origin[1]][origin[2]] = temp_icon
                                    self.inventory_bag_stack_text[origin[1]][origin[2]] = temp_text
                            self.inventory_list[row][col] = self.dragging_item
                            self.inventory_bag_icon[row][col] = self.dragging_item['icon']
                            self.inventory_bag_stack_text[row][col] = self.font.render(str(self.dragging_item['quantity']), True, (255, 255, 255))
                            self.dragging_item = None
                            self.drag_start_pos = None
                            break


    '''                        
    '''
    def handle_mouse_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Vérifier si la souris est sur un slot de la barre d'inventaire
            for i in range(10):  # Barre d'inventaire avec 10 slots
                if self.is_mouse_on_slot(485 + i * 60, self.screen.get_height() - 90, 50, 50):
                    if self.inventory_bar_list[i]:
                        self.dragging_item = self.inventory_bar_list[i]  # Assurez-vous que l'objet est stocké ici
                        self.dragging_item['icon'] = self.inventory_icons[i]  # Ajoutez l'icône ici
                        self.drag_start_pos = ("bar", i)
                        self.inventory_bar_list[i] = {}
                        self.inventory_icons[i] = pygame.image.load(f"Items/slot.png")
                        self.stack_text[i] = pygame.image.load(f"Items/slot.png")

            # Vérifier si la souris est sur un slot de l'inventaire 6x5
            for row in range(5):  # 5 lignes
                for col in range(6):  # 6 colonnes
                    if self.is_mouse_on_slot(595 + col * (self.CELL_SIZE + self.CELL_SPACING), 290 + row * (self.CELL_SIZE + self.CELL_SPACING), self.CELL_SIZE, self.CELL_SIZE):
                        if self.inventory_list[row][col]:
                            self.dragging_item = self.inventory_list[row][col]  # Assurez-vous que l'objet est stocké ici
                            self.dragging_item['icon'] = self.inventory_bag_icon[row][col]  # Ajoutez l'icône ici
                            self.drag_start_pos = ("bag", row, col)
                            self.inventory_list[row][col] = {}

                            self.inventory_bag_icon[row][col] = pygame.image.load("Items/slot.png")
                            self.inventory_bag_stack_text[row][col] = pygame.image.load("Items/slot.png")

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Déposer l'objet dans la barre d'outils
            for i in range(10):  # Barre d'inventaire avec 10 slots
                if self.is_mouse_on_slot(485 + i * 60, self.screen.get_height() - 90, 50, 50):
                    if self.dragging_item :
                        self.inventory_bar_list[i] = self.dragging_item
                        self.inventory_icons[i] = self.inventory_bar_list[i]['icon']
                        self.stack_text[i]= self.font.render(str(self.inventory_bar_list[i]['quantity']), True, (255, 255, 255))
                        self.dragging_item = None
                        self.drag_start_pos = None

                        break

            # Déposer dans l'inventaire 6x5
            for row in range(5):  # 5 lignes
                for col in range(6):  # 6 colonnes
                    if self.is_mouse_on_slot(595 + col * (self.CELL_SIZE + self.CELL_SPACING), 290 + row * (self.CELL_SIZE + self.CELL_SPACING), self.CELL_SIZE, self.CELL_SIZE):
                        if self.dragging_item:
                            self.inventory_list[row][col] = self.dragging_item
                            self.inventory_bag_icon[row][col] = self.inventory_list[row][col]['icon']
                            self.inventory_bag_stack_text[row][col]= self.font.render(str(self.inventory_list[row][col]['quantity']), True, (255, 255, 255))
                            self.dragging_item = None
                            self.drag_start_pos = None
                            break
        '''





