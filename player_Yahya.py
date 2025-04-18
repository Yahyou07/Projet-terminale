
import pygame
import math
import time
class Player(pygame.sprite.Sprite): 
    def __init__(self,pos_x,pos_y,screen):
        super().__init__()  # Initialisation du sprite
        
        self.speed = 3
        self.speed_run = 4.5
        self.screen = screen
        self.health_value = 50
        self.mana_value = 0
        self.endurance_value = 100
        self.font = pygame.font.Font("Items/Minecraft.ttf", 14)  # Police par défaut, taille 14
        self.font_book = pygame.font.Font("Items/Minecraft.ttf", 20)  # Police par défaut, taille 20
        self.font_fantasy = pygame.font.Font("Items/Minecraft.ttf", 45)  # Police par défaut, taille 20
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
        self.armour_list = [{} for i in range(4)]
        self.armour_icon_list = [pygame.image.load("UI/Inventories/casque_ic.png"),pygame.image.load("UI/Inventories/plastron_ic.png"),pygame.image.load("UI/Inventories/jambiere_ic.png"),pygame.image.load("UI/Inventories/bottes_ic.png")]
        self.armour_icon_list2 = [pygame.image.load("UI/Inventories/casque_ic.png"),pygame.image.load("UI/Inventories/plastron_ic.png"),pygame.image.load("UI/Inventories/jambiere_ic.png"),pygame.image.load("UI/Inventories/bottes_ic.png")]
        #Tableaux de l'inventaire :
        # Inventaire étendu (sac) : 6 colonnes × 5 lignes = 30 emplacements
        self.inventory_list = [[{} for _ in range(6)] for _ in range(5)]
        self.inventory_bag_icon = [[pygame.image.load("Items/slot.png") for _ in range(6)] for _ in range(5)]
        self.inventory_bag_stack_text = [[self.font.render("", True, (255, 255, 255)) for _ in range(6)] for _ in range(5)]
        
        self.inventory_index = 0
        self.current_item = self.inventory_bar_list[self.inventory_index]
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
        self.attack_left_mouv = [pygame.image.load(f"animation/attack/attack2/left{j}.png") for j in range(1, 6)]

        #Index que l'on utlise pour l'animation
        self.current_sprite = 0
        #On prend comme image de base idle1
        self.image = pygame.image.load("animation/idle/idle1/down1.png")

        #Paramètres du joueur rect, position ...
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

        

        # Charger l'image du curseur de l'inventaire
        self.cursor_image = pygame.image.load("UI/Inventories/cursor.png")

        #On charge ici les images des bouttons pour les quete, livre ...
        self.button_book = pygame.image.load("UI/boutton_book.png")
        self.rect_button_book = self.button_book.get_rect()
        self.rect_button_book.x = 1510
        self.rect_button_book.y = 100

        self.button_quete = pygame.image.load("UI/boouton_q.png")
        self.rect_button_quete = self.button_quete.get_rect()

        self.button_map = pygame.image.load("UI/boouton_m.png")
        self.rect_button_map = self.button_map.get_rect()

        # On charge ici les images utilisées pour l'interface du livre
        self.OnBook = False
        self.fond_table = pygame.image.load("UI/livre/table.png")
        self.fond_table = pygame.transform.scale(self.fond_table,(self.screen.get_width(),self.screen.get_height()))
        self.button_back_book = pygame.image.load("UI/button_back.png")
        self.rect_button_back_book = self.button_back_book.get_rect()
        self.rect_button_back_book.x = 5
        self.rect_button_back_book.y = 10
        
        self.open_book = [pygame.image.load(f"UI/livre/open_book/frame_{j}.png") for j in range(0, 8)]
        self.turn_left = [pygame.image.load(f"UI/livre/turn_right1/frame_{j}.png") for j in range(0, 8)]
        self.turn_right = [pygame.image.load(f"UI/livre/turn_left/frame_{j}.png") for j in range(0, 8)]
        
        self.current_book_index = 0
        self.current_book = self.open_book[self.current_book_index]
        
        self.current_book = pygame.transform.scale(self.current_book,(800,750))
        
        self.IsAnimating = True
        self.IsOpen = False
        
        self.button_right_book = pygame.image.load("UI/bouton_droitBook.png")
        self.rect_button_right_book = self.button_right_book.get_rect()
        self.rect_button_right_book.x = 900
        self.rect_button_right_book.y = 740

        self.button_left_book = pygame.image.load("UI/bouton_gaucheBook.png")
        self.rect_button_left_book = self.button_left_book.get_rect()
        self.rect_button_left_book.x = 660
        self.rect_button_left_book.y = 740
        self.page = 0
        self.page_a_cote = self.page + 1
        self.max_page = 20
        self.pages_text = self.font_fantasy.render(f"{str(self.page)} - {self.page_a_cote}",True, (255, 174, 111))

        self.pages = [self.font_book .render("Salut chef",True, (255, 255, 111)),
                      self.font_book .render("Salut le singe",True, (255, 255, 111)), 
                      self.font_book .render("Salut l'arabe",True, (255, 255, 111)),
                      self.font_book .render("Salut Michel",True, (255, 255, 111)),
                      self.font_book .render("Salut Roger",True, (255, 255, 111)),
                      self.font_book .render("Salut Renoisanseaux",True, (255, 255, 111)),
                      self.font_book .render("Salut Janny",True, (255, 255, 111)),
                      self.font_book .render("Salut Gros",True, (255, 255, 111))
                      ]

        self.book_animation_list = []
        self.book_anim_speed = 0
        self.book_anim_index = 0
        self.book_animating = False
        self.Affiche_texte_page = True
        
        self.anim_move_player = []
        self.player_speed_anim = 0
        self.player_index_anim = 0
        self.player_attack_anim = False
        self.decalement = 5

        self.hache_anim = [pygame.image.load(f"UI/hache/frame_{j}.png") for j in range(0, 40)]
        self.current_hache = 0
        self.hache = pygame.image.load("UI/hache/frame_0.png")
        self.hache = pygame.transform.scale(self.hache,(140,140))

    def start_anim_attack(self,list_mouv,speed,decal):
        '''
        Dans cette méthode on va remplacer certaine les variables utilisées dans anim_player_full_animation (list_mouv et speed)
        par les paramètre présents dans la méthode que l'on pourra changer dynamiquement selon le mouvement
        On remet également player_attack_anim à True pour relancer la méthode à chaque fois qu'on le souhaite.

        '''
        self.anim_move_player = list_mouv
        self.player_speed_anim = speed
        self.player_index_anim = 0
        self.player_attack_anim = True
        self.decalment = decal
    def startBookAnimation(self, liste_mouv, speed):
        
        self.book_animation_list = liste_mouv
        self.book_anim_speed = speed
        self.book_anim_index = 0
        self.book_animating = True
        self.IsOpen = False
        self.Affiche_texte_page = False

    def animation(self,liste_mouv,speed):
        self.current_sprite += speed
        if self.current_sprite >=len(liste_mouv):
            self.current_sprite = 0
        self.image = liste_mouv[int(self.current_sprite)]


    def animation_hache(self,liste_mouv,speed):
        self.current_hache += speed
        if self.current_hache >=len(liste_mouv):
            self.current_hache = 0
        self.hache = liste_mouv[int(self.current_hache)]
        self.hache = pygame.transform.scale(self.hache,(140,140))
    
    def animBook(self):
        if self.book_animating:
            self.book_anim_index += self.book_anim_speed
            if self.book_anim_index >= len(self.book_animation_list):
                self.book_animating = False
                self.IsOpen = True
                self.book_anim_index = len(self.book_animation_list) - 1  # Assurez-vous que l'index est dans les limites
                print('en train d animer')
                self.Affiche_texte_page = True
            elif self.book_anim_index < 0:
                self.book_anim_index = 0  # Assurez-vous que l'index n'est pas négatif
            self.current_book = self.book_animation_list[int(self.book_anim_index)]
            print(self.current_book)
            self.current_book = pygame.transform.scale(self.current_book, (800, 750))  # Appliquez l'échelle ici

    def anim_player_full_animation(self):
        if self.player_attack_anim:
            self.player_index_anim += self.player_speed_anim
            self.rect.x += self.decalment
            # Si l'index est supérieur a la taille de la liste de mouvement :
            if self.player_index_anim >= len(self.anim_move_player):
                
                self.player_attack_anim = False # Alors on arrete le processus en mettant le booleen a False
                self.player_index_anim = len(self.anim_move_player) - 1  #Et on desincrémente l'index pour ne pas être out of range

            # Si l'index est négatif     
            elif self.player_index_anim < 0: 
                self.player_index_anim = 0  # Alors on le remet a zero
            self.image = self.anim_move_player[int(self.player_index_anim)] # On change l'image de base par l'image de la liste de mouvment du current_index
            

    

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
        if 0 < self.health_value <= 20:
            self.current_health = self.health[5]
        elif 20 < self.health_value <= 40:
            self.current_health = self.health[4]
        elif 40 < self.health_value <= 60:
            self.current_health = self.health[3]
        elif 60 < self.health_value <= 80:
            self.current_health = self.health[2]
    
        elif 80 < self.health_value <= 99:
            self.current_health = self.health[1]
        elif self.health_value == 100:
            self.current_health = self.health[0]
        elif self.health_value == 0:
            self.current_health = self.health[6]

        if self.health_value < 1:
            self.health_value = 0
        elif self.health_value > 99:
            self.health_value = 100
        #####
        #####
         #Gestion affichage de la barre de mana selon la valeur de la mana
        if 0 < self.mana_value <= 20:
            self.current_mana = self.mana[4]

        elif 20 < self.mana_value <= 40:
            self.current_mana = self.mana[3]

        elif 40 < self.mana_value <= 60:
            self.current_mana = self.mana[2]

        elif 60 < self.mana_value <= 80:
            self.current_mana = self.mana[1]
    
        elif self.mana_value == 100:
            self.current_mana = self.mana[0]

        elif self.mana_value == 0:
            self.current_mana = self.mana[5]

        if self.mana_value < 1:
            self.mana_value = 0
        elif self.mana_value > 99:
            self.mana_value = 100
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
        
        x = self.screen.get_width()-0.696875*self.screen.get_width()
        for icon in self.inventory_icons:
            self.screen.blit(icon,(x,self.screen.get_height()-0.09*self.screen.get_height()))
            x += 60
        
        x_stack = self.screen.get_width()-0.675*self.screen.get_width()
        for stack in self.stack_text:
            self.screen.blit(stack,(x_stack,self.screen.get_height()-0.07*self.screen.get_height()))
            x_stack += 60
        
        # Afficher le curseur
        cursor_x = self.INV_X + self.inventory_index * (self.CELL_SIZE + 10)
        cursor_y = self.INV_Y
        self.screen.blit(self.cursor_image, (cursor_x, cursor_y))
        
        self.current_item = self.inventory_bar_list[self.inventory_index]

        # Affichage des bouttons sur le cote
        self.screen.blit(self.button_book,(1520,100))
        self.screen.blit(self.button_quete,(1538,200))
        self.screen.blit(self.button_map,(1538,300))

        if self.OnBook:
            self.screen.blit(self.fond_table, (0, 0))
            self.screen.blit(self.current_book, (400, -40))
            self.screen.blit(self.button_back_book, (5, 10))
            

            if self.IsOpen:
                self.screen.blit(self.button_right_book, (900, 740))
                self.screen.blit(self.button_left_book, (660, 740))
                self.pages_text = self.font_fantasy.render(f"{str(self.page)} - {self.page_a_cote}",True, (255, 174, 111))
                self.screen.blit(self.pages_text,(760,750))

                if self.Affiche_texte_page:
                    self.screen.blit(self.pages[self.page],(513,300))
                    self.screen.blit(self.pages[self.page_a_cote],(840,300))

        

    def is_mouse_on_slot(self, x, y, width, height):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return x <= mouse_x <= x + width and y <= mouse_y <= y + height
    
    def display_inventory(self):
        
        if self.OnBag:
            # Affichage de l'image de l'inventaire
            x = self.screen.get_width() // 2 - self.inventory_image.get_width() // 2 - 50
            y = self.screen.get_height() // 2 - self.inventory_image.get_height() // 2
            self.screen.blit(self.inventory_image, (x, y))

            start_x =  self.screen.get_width()-self.screen.get_width()*0.628125  # Position X de la première cellule
            start_y = self.screen.get_height()-self.screen.get_height()*0.6777777  # Position Y de la première cellule
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
            
            x_icon = self.screen.get_width()-0.49375*self.screen.get_width()
            y_icon =  self.screen.get_height()- self.screen.get_height()*0.6777777
            for i in self.armour_icon_list:
                self.screen.blit(i,(x_icon,y_icon))
                y_icon +=73

            # Si un objet est en cours de glisser-déposer, afficher l'icône à la position de la souris
            if self.dragging_item and 'icon' in self.dragging_item:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Afficher l'icône de l'item au-dessus de la souris
                self.screen.blit(self.dragging_item['icon'], (mouse_x - self.CELL_SIZE // 2, mouse_y - self.CELL_SIZE // 2))


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
                    self.inventory_bar_list[i] = {'name': sprite.name,'object':sprite ,'quantity': stack_total,'icon':sprite.icon}
                    self.inventory_icons[i] = sprite.icon
                    self.stack_text[i] = self.font.render(str(stack_total), True, (255, 255, 255))
                    found = True
                break

        if not found:
            # Chercher un slot vide dans la barre
            for i in range(len(self.inventory_bar_list)):
                slot = self.inventory_bar_list[i]
                if not slot or slot.get("name") == "rien":
                    self.inventory_bar_list[i] = {'name': sprite.name,'object':sprite , 'quantity': 1,'icon':sprite.icon}
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
                            self.inventory_list[row][col] = {'name': sprite.name,'object':sprite , 'quantity': stack_total,'icon':sprite.icon}
                            self.inventory_bag_icon[row][col] = sprite.icon
                            self.inventory_bag_stack_text[row][col] = self.font.render(str(stack_total), True, (255, 255, 255))
                            return

            # Sinon, chercher un slot vide dans le sac
            for row in range(5):
                for col in range(6):
                    slot = self.inventory_list[row][col]
                    if not slot or slot.get("name") == "rien":
                        self.inventory_list[row][col] = {'name': sprite.name,'object':sprite , 'quantity': 1,'icon':sprite.icon}
                        self.inventory_bag_icon[row][col] = sprite.icon
                        self.inventory_bag_stack_text[row][col] = self.font.render("1", True, (255, 255, 255))
                        return


    def restore_item(self, origin, item):
        if origin[0] == "bar":
            self.inventory_bar_list[origin[1]] = item
            self.inventory_icons[origin[1]] = item['icon']
            self.stack_text[origin[1]] = self.font.render(str(item['quantity']), True, (255, 255, 255))
        elif origin[0] == "bag":
            self.inventory_list[origin[1]][origin[2]] = item
            self.inventory_bag_icon[origin[1]][origin[2]] = item['icon']
            self.inventory_bag_stack_text[origin[1]][origin[2]] = self.font.render(str(item['quantity']), True, (255, 255, 255))
        elif origin[0] == "armour":
            self.armour_list[origin[1]] = item
            self.armour_icon_list[origin[1]] = item['icon']


        # Méthode pour mettre à jour la mana en fonction de l'armure
    def update_mana_on_armour_change(self, slot_index, remove=False):
        # Valeurs de mana associées aux armures
        armour_mana_values = {
            0: 30,  # Casque
            1: 40,  # Plastron
            2: 20,  # Jambière
            3: 10   # Bottes
        }
        
        if remove:
            # Si on retire une armure, on diminue la mana
            self.mana_value -= armour_mana_values[slot_index]
        else:
            # Si on ajoute une armure, on augmente la mana
            self.mana_value += armour_mana_values[slot_index]

        # On s'assure que la mana ne devienne pas négative
        self.mana_value = max(self.mana_value, 0)
        print(f"Mana Value: {self.mana_value}")  # Pour vérifier

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
                        self.stack_text[i] = self.font.render("", True, (255, 255, 255))

            # Clic sur sac
            if self.OnBag:
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
                                self.inventory_bag_stack_text[row][col] = self.font.render("", True, (255, 255, 255))

            # Clic sur armure
            if self.OnArmour:
                for i in range(len(self.armour_list)):
                    if self.is_mouse_on_slot(800, 288 + i * 70, 50, 50):
                        if self.armour_list[i]:
                            self.dragging_item = self.armour_list[i]
                            self.dragging_item['icon'] = self.armour_icon_list[i]
                            self.drag_start_pos = ("armour", i)
                            self.armour_list[i] = {}
                            self.armour_icon_list[i] = self.armour_icon_list2[i]
                            self.update_mana_on_armour_change(i, remove=True)  # On retire la mana lorsque l'armure est enlevée
           
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Toujours gérer les échanges dans la barre
            if self.dragging_item:
                for i in range(10):
                    if self.is_mouse_on_slot(485 + i * 60, self.screen.get_height() - 90, 50, 50):
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
                        if slot:
                            self.restore_item(self.drag_start_pos, slot)
                        self.inventory_bar_list[i] = self.dragging_item
                        self.inventory_icons[i] = self.dragging_item['icon']
                        self.stack_text[i] = self.font.render(str(self.dragging_item['quantity']), True, (255, 255, 255))
                        self.dragging_item = None
                        self.drag_start_pos = None
                        return

            if self.OnBag:
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
                                if slot:
                                    self.restore_item(self.drag_start_pos, slot)
                                self.inventory_list[row][col] = self.dragging_item
                                self.inventory_bag_icon[row][col] = self.dragging_item['icon']
                                self.inventory_bag_stack_text[row][col] = self.font.render(str(self.dragging_item['quantity']), True, (255, 255, 255))
                                self.dragging_item = None
                                self.drag_start_pos = None
                                return

            if self.OnArmour:
                for i in range(len(self.armour_list)):
                    if self.is_mouse_on_slot(800, 288 + i * 70, 50, 50):
                        if self.dragging_item:
                            correct_type = (
                                (i == 0 and self.dragging_item['object'].type == "Casque") or
                                (i == 1 and self.dragging_item['object'].type == "Plastron") or
                                (i == 2 and self.dragging_item['object'].type == "Jambiere") or
                                (i == 3 and self.dragging_item['object'].type == "Bottes")
                            )
                            if correct_type:
                                slot = self.armour_list[i]
                                if slot and slot['name'] == self.dragging_item['name']:
                                    total = slot['quantity'] + self.dragging_item['quantity']
                                    stack_max = slot['object'].stack_max
                                    if total <= stack_max:
                                        slot['quantity'] = total
                                        
                                        self.dragging_item = None
                                        self.drag_start_pos = None
                                        return
                                if slot:
                                    self.restore_item(self.drag_start_pos, slot)
                                self.armour_list[i] = self.dragging_item
                                self.armour_icon_list[i] = self.dragging_item['icon']
                                self.update_mana_on_armour_change(i, remove=False)  # On ajoute la mana quand l'armure est posée
                                self.dragging_item = None
                                self.drag_start_pos = None
                                return
                            else:
                                self.restore_item(self.drag_start_pos, self.dragging_item)
                                self.dragging_item = None
                                self.drag_start_pos = None
                                return

            # Si on lâche nulle part
            if self.dragging_item and self.drag_start_pos:
                self.restore_item(self.drag_start_pos, self.dragging_item)
                self.dragging_item = None
                self.drag_start_pos = None


    def handle_key_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.inventory_index = 0
                print(self.current_item)
            elif event.key == pygame.K_2:
                self.inventory_index = 1
                print(self.current_item)
            elif event.key == pygame.K_3:
                self.inventory_index = 2
                print(self.current_item)
            elif event.key == pygame.K_4:
                self.inventory_index = 3
                print(self.current_item)
            elif event.key == pygame.K_5:
                self.inventory_index = 4
                print(self.current_item)
            elif event.key == pygame.K_6:
                self.inventory_index = 5
                print(self.current_item)
            elif event.key == pygame.K_7:
                self.inventory_index = 6
                print(self.current_item)
            elif event.key == pygame.K_8:
                self.inventory_index = 7
                print(self.current_item)
            elif event.key == pygame.K_9:
                self.inventory_index = 8
                print(self.current_item)
            elif event.key == pygame.K_0:
                self.inventory_index = 9
                print(self.current_item)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Molette vers le haut
                self.inventory_index = (self.inventory_index + 1) % 10
                print(self.current_item)
            elif event.button == 5:  # Molette vers le bas
                self.inventory_index = (self.inventory_index - 1) % 10
                print(self.current_item)

    #Méthode eat pour consommer des items de type Food
    def eat(self, index):
        # Vérifiez si l'index est dans la barre d'inventaire et que la vie est inferieure a 100
        if 0 <= index < len(self.inventory_bar_list) and self.health_value < 100:
            item = self.inventory_bar_list[index]
            if item and item['object'].type == "Food":
                # Décrémentez la quantité de l'item
                item["quantity"] -= 1
                self.health_value += item["object"].regen
                if item["quantity"] <= 0:
                    # Si la quantité est 0, supprimez l'item de l'inventaire
                    self.inventory_bar_list[index] = {}
                    self.inventory_icons[index] = pygame.image.load("Items/slot.png")
                    self.stack_text[index] = self.font.render("", True, (255, 255, 255))
                else:
                    # Mettez à jour l'affichage de la quantité
                    self.stack_text[index] = self.font.render(str(item["quantity"]), True, (255, 255, 255))
                print(f"Mange {item['object'].name}. Quantite restante: {item['quantity']}")
            
        


   