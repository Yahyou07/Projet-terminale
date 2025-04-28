import pygame
from effect import *
from objects_Yahya import *
from math import *
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
    def __init__(self,name,x,y,type,screen,scale):
        super().__init__()
        self.name = name
        self.image = pygame.image.load(f"{type}/{name}/idle/idle1.png")
        #mouvement basique de l'enemy walk
        self.right_move = [pygame.image.load(f"{type}/{name}/walk/walk1/right{i}.png")for i in range(1,10)]
        self.left_move = [pygame.image.load(f"{type}/{name}/walk/walk2/left{i}.png")for i in range(1,10)]
        self.top_move = [pygame.image.load(f"{type}/{name}/walk/walk3/top{i}.png")for i in range(1,10)]
        self.bottom_move = [pygame.image.load(f"{type}/{name}/walk/walk4/bottom{i}.png")for i in range(1,10)]
        

        self.idle_move = [pygame.image.load(f"{type}/{name}/idle/idle{i}.png")for i in range(1,4)]
                # Détection automatique de la taille d'origine
        original_width, original_height = self.image.get_size()

        # Si l'image est grande (128px), alors on réduit moins fort
        if original_width == 128:
            self.image = pygame.transform.scale(self.image, scale)  # 64x64 visuellement
        elif original_width == 64:
            self.image = pygame.transform.scale(self.image, scale)  # 50x50 visuellement

        self.rect = self.image.get_rect()
        
        

        self.rect.center = (x, y)
        
        self.sprite_index = 0
        
        self.screen = screen
        self.distance_between_player_slime = None


    def animation(self,list_mouv,speed,scale):
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
        self.image = pygame.transform.scale(self.image,scale)

    def droite(self):
        """
            Déplacement de l'entité vers la droite
        """
        self.rect.x += 1
        self.animation(self.right_move,0.20,(50,50))
        
    def idle(self):
        """
            Animation idle de l'entité
        """
        self.animation(self.idle_move,0.12,(50,50))

    def haut(self):
        """
            Déplacement de l'entité vers le haut
        """
        self.rect.y -= 1
        self.animation(self.top_move,0.20,(50,50))

    def bas(self):
        """
            Déplacement de l'entité vers le bas
        """
        self.rect.y += 1
        self.animation(self.bottom_move,0.2,(50,50))

    def gauche(self):
        """
            Déplacement de l'entité vers la gauche
        """
        self.rect.x -= 1
        self.animation(self.left_move,0.2,(50,50))

    

class PNJ(Entity):
    def __init__(self, name, x, y, type, screen,scale,parole):
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
        super().__init__(name, x, y, type, screen,scale)
        self.hit_box = self.rect.copy().inflate(-30,0)
        self.champ_vision = self.rect.copy().inflate(20,20)

        self.dialog_box = pygame.image.load("UI/dialog_box_gris.png")
        self.dialog_box_name = pygame.image.load("UI/dialog_box_nom.png")
        self.portrait = pygame.image.load(f"{type}/{name}/portrait.png")
        
        self.font_dialog_box_name = pygame.font.Font("UI/dialog_font.ttf", 20)
        self.font_dialog_box = pygame.font.Font("UI/dialog_font.ttf", 15)
        self.font_dialog_box_pass = pygame.font.Font("UI/dialog_font.ttf", 13)
        self.CanDialog = False
        

        self.current_text = ""    # Le texte affiché progressivement
        self.full_text = ""       # Le texte complet à afficher
        self.text_index = 0       # Où on en est dans le texte
        self.last_update_time = pygame.time.get_ticks()  # Pour gérer la vitesse
        self.text_speed = 30      # Millisecondes entre chaque lettre (plus petit = plus rapide)
        self.current_parole_index = 0  # Numéro de la phrase actuelle
    
        self.parole = parole
        self.message_passer = "[ESPACE] pour passer"
        self.name_entity = self.font_dialog_box_name.render(self.name,True, (255, 255, 111))
        self.entity_parole = self.font_dialog_box.render(self.parole[3],True, (255, 255, 111))
        self.pass_message = self.font_dialog_box_pass.render(self.message_passer,True, (255, 255, 255))
        
    def update(self,dt):
        """
            Met à jour l'entité
        """
        if self.CanDialog:
            self.screen.blit(self.dialog_box,(300,600))
            self.screen.blit(self.portrait,(360,500))
            self.screen.blit(self.dialog_box_name,(350,750))
            self.screen.blit(self.name_entity,(410,770))
            
            if self.parole.index == len(self.parole)-1:
                self.pass_message = self.font_dialog_box_pass.render("[ESPACE] pour quitter",True, (255, 255, 255))
                self.screen.blit(self.pass_message,(680,780))
            else:
                self.pass_message = self.font_dialog_box_pass.render("[ESPACE] pour passer",True, (255, 255, 255))
                self.screen.blit(self.pass_message,(680,780))


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
    def __init__(self, name, x, y, type, screen,scale):
        super().__init__(name, x, y, type, screen,scale)

        #mouvements d'attaque de l'ennemi 
        self.right_attack = [pygame.image.load(f"{type}/{name}/attack/attack1/right{i}.png")for i in range(1,7)]
        self.left_attack = [pygame.image.load(f"{type}/{name}/attack/attack2/left{i}.png")for i in range(1,7)]
        self.top_attack = [pygame.image.load(f"{type}/{name}/attack/attack3/top{i}.png")for i in range(1,7)]
        self.bottom_attack =[pygame.image.load(f"{type}/{name}/attack/attack4/bottom{i}.png")for i in range(1,7)]

        #mouvement de mort à voir si on l'intègre
        self.dead_mouve = [pygame.image.load(f"{type}/{name}/dead/dead{i}.png")for i in range(1,7)]
        self.champ_vision_enemy = self.rect.copy().inflate(300, 300)  # Champ de vision agrandi autour de l'ennemi
        self.speed = 1  # Vitesse de déplacement vers le joueur
        self.detected_player = False  # Si le joueur est détecté
        
        self.hitbox = self.rect.copy().inflate(-80, -80)
        
        self.hit_box = self.rect.copy().inflate(0,0)


        self.max_health = 60  # Vie maximale
        self.current_health = 60  # Vie actuelle
        self.health_bar_width = 60  # Largeur de la barre de vie
        self.health_bar_height = 10   # Hauteur de la barre
        self.last_dir = "down"

        self.knockback = False    # Est-ce que l'ennemi est repoussé
        self.knockback_speed = 0  # Vitesse actuelle du recul
        self.knockback_direction = 0  # Direction du recul : -1 pour gauche, 1 pour droite

        self.distance_between_player_enemy = None
        self.attack_cooldown = 1000  # 1000 ms = 1 seconde entre 2 attaques
        self.last_attack_time = 0  # Dernier moment où l'ennemi a attaqué
    def animation_attack(self,list_mouv,speed,scale,player,dirx,diry):
        """
            Animation de l'entité
            Attributs:
                list_mouv : liste des images de l'animation
                speed : vitesse de l'animation
        """
        self.sprite_index += speed
        if self.sprite_index >=len(list_mouv):
            self.sprite_index = 0
            player.knockback = True
            player.knockback_speed = 5
            player.knockback_direction = dirx
            player.knockback_direction_y = diry
        self.image = list_mouv[int(self.sprite_index)]
        self.image = pygame.transform.scale(self.image,scale)

    def draw_health_bar(self, screen, map_layer):
        """ Dessine la barre de vie arrondie de l'ennemi au-dessus de lui """
        world_pos = (self.rect.centerx, self.rect.top - 10)
        screen_pos = map_layer.translate_point(world_pos)

        health_percentage = self.current_health / self.max_health

        # Fond de la barre (rouge clair)
        bg_rect = pygame.Rect(0, 0, self.health_bar_width, self.health_bar_height)
        bg_rect.center = screen_pos
        pygame.draw.rect(screen, (200, 50, 50), bg_rect, border_radius=3)

        # Barre de vie (verte)
        health_rect = pygame.Rect(0, 0, self.health_bar_width * health_percentage, self.health_bar_height)
        health_rect.topleft = bg_rect.topleft
        health_rect.height = self.health_bar_height
        pygame.draw.rect(screen, (50, 205, 50), health_rect, border_radius=3)


        
    def dead(self, group, sprite):
        smoke = Effect("fumee","frame_",self.rect.centerx, self.rect.centery,(100,100))
        group.add(smoke)
        group.remove(sprite)
        

        
    def idle_enemy(self):
        """
            Animation idle de l'entité
        """
        self.animation(self.idle_move,0.12,(100,100))

    def follow_player(self, player, all_enemies):
        """ Fait bouger l'ennemi vers le joueur en diagonale avec évitement basé sur hitbox """
        self.distance_between_player_enemy = sqrt((player.rect.centerx - self.rect.centerx)**2 +(player.rect.centery - self.rect.centery)**2)
        
        # Met à jour la hitbox
        self.hitbox.center = self.rect.center
        
        if self.champ_vision_enemy.colliderect(player.hit_box):
            self.detected_player = True
        else:
            self.detected_player = False

        if self.detected_player and not player.dead:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery

            if self.distance_between_player_enemy <= 30:
                now = pygame.time.get_ticks()
                if abs(dx) > abs(dy):
                    if dx > 0:
                        self.animation_attack(self.right_attack, 0.15, (100, 100),player,1,0)
                        self.last_dir = "right"
                    else:
                        self.animation_attack(self.left_attack, 0.15, (100, 100),player,-1,0)
                        self.last_dir = "left"
                else:
                    if dy > 0:
                        self.animation_attack(self.bottom_attack, 0.15, (100, 100),player,0,1)
                        self.last_dir = "down"
                    else:
                        self.animation_attack(self.top_attack, 0.15, (100, 100),player,0,-1)
                        self.last_dir = "up"

                if now - self.last_attack_time > self.attack_cooldown:
                    player.health_value -= 15
                    if player.health_value < 0:
                        player.health_value = 0
                    self.last_attack_time = now

            else:
                # EVITEMENT avec hitbox
                for other in all_enemies:
                    if other is not self and self.hitbox.colliderect(other.hitbox):
                        if self.rect.centerx < other.rect.centerx:
                            self.rect.x -= 1
                        else:
                            self.rect.x += 1

                        if self.rect.centery < other.rect.centery:
                            self.rect.y -= 1
                        else:
                            self.rect.y += 1

                # DEPLACEMENT NORMAL
                if abs(dx) > abs(dy):
                    if dx > 0:
                        self.rect.x += self.speed
                        self.animation(self.right_move, 0.2, (100, 100))
                        self.last_dir = "right"
                    else:
                        self.rect.x -= self.speed
                        self.animation(self.left_move, 0.2, (100, 100))
                        self.last_dir = "left"
                else:
                    if dy > 0:
                        self.rect.y += self.speed
                        self.animation(self.bottom_move, 0.2, (100, 100))
                        self.last_dir = "down"
                    else:
                        self.rect.y -= self.speed
                        self.animation(self.top_move, 0.2, (100, 100))
                        self.last_dir = "up"
        else:
            self.idle_enemy()





class Slime(pygame.sprite.Sprite):
    def __init__(self,name,type,x,y):
        super().__init__()
        
        self.name = name
        self.image = pygame.image.load(f"{type}/{name}/walk/walk4/bottom1.png")
        
        #mouvement basique du slime walk
        self.right_move = [pygame.image.load(f"{type}/{name}/walk/walk1/right{i}.png")for i in range(1,25)]
        self.left_move = [pygame.image.load(f"{type}/{name}/walk/walk2/left{i}.png")for i in range(1,25)]
        self.top_move = [pygame.image.load(f"{type}/{name}/walk/walk3/top{i}.png")for i in range(1,25)]
        self.bottom_move = [pygame.image.load(f"{type}/{name}/walk/walk4/bottom{i}.png")for i in range(1,25)]
        

        self.idle_move = [pygame.image.load(f"{type}/{name}/walk/walk4/bottom{i}.png")for i in range(1,25)]
        self.image = pygame.transform.scale(self.image,(40,40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.sprite_index = 0
        self.champ_vision_enemy = self.rect.copy().inflate(500, 500)  # Champ de vision agrandi autour de l'ennemi
        self.speed = 1.3  # Vitesse de déplacement vers le joueur
        self.detected_player = False  # Si le joueur est détecté

        self.max_health = 20  # Vie maximale
        self.current_health = 20  # Vie actuelle
        self.health_bar_width = 20  # Largeur de la barre de vie
        self.health_bar_height = 10   # Hauteur de la barre


    def draw_health_bar(self, screen, map_layer):
        """ Dessine la barre de vie arrondie de l'ennemi au-dessus de lui """
        world_pos = (self.rect.centerx, self.rect.top - 10)
        screen_pos = map_layer.translate_point(world_pos)

        health_percentage = self.current_health / self.max_health

        # Fond de la barre (rouge clair)
        bg_rect = pygame.Rect(0, 0, self.health_bar_width, self.health_bar_height)
        bg_rect.center = screen_pos
        pygame.draw.rect(screen, (200, 50, 50), bg_rect, border_radius=3)

        # Barre de vie (verte)
        health_rect = pygame.Rect(0, 0, self.health_bar_width * health_percentage, self.health_bar_height)
        health_rect.topleft = bg_rect.topleft
        health_rect.height = self.health_bar_height
        pygame.draw.rect(screen, (50, 205, 50), health_rect, border_radius=3)

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
        self.image = pygame.transform.scale(self.image,(40,40))

    def idle(self):
        self.animation(self.bottom_move,1)
        
    def follow_player(self, player):
        """ Fait bouger l'ennemi vers le joueur en diagonale avec bonne animation """

        self.distance_between_player_slime = sqrt((player.rect.centerx - self.rect.centerx)**2 +(player.rect.centery - self.rect.centery)**2)
        
        if self.champ_vision_enemy.colliderect(player.hit_box):
            self.detected_player = True
        else:
            self.detected_player = False

        if self.detected_player:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery

            # Déplacement en X et Y
            if dx != 0:
                self.rect.x += self.speed if dx > 0 else -self.speed
            if dy != 0:
                self.rect.y += self.speed if dy > 0 else -self.speed

            # Animation : choisir la plus grande distance
            if abs(dx) > abs(dy):
                if dx > 0:
                    self.animation(self.right_move, 1)
                    self.last_dir = "right"
                else:
                    self.animation(self.left_move, 1)
                    self.last_dir = "left"
            else:
                if dy > 0:
                    self.animation(self.bottom_move, 1)
                    self.last_dir = "down"
                else:
                    self.animation(self.top_move, 1)
                    self.last_dir = "up"

        else:
            self.idle()   
    def kamikaze(self,sprite,group,player):
        explosion = Effect("explosion","frame",self.rect.centerx, self.rect.centery,(150,150))
        crater = Crater("crater",self.rect.centerx-40,self.rect.centery)
        
        group.add(crater,layer = 3)
        group.add(explosion,layer = 6)
        if player.last_direction == "right":
            player.knockback = True
            player.knockback_speed = 10
            player.knockback_direction = -1
            player.knockback_direction_y = 0

        if player.last_direction == "left" :
            player.knockback = True
            player.knockback_speed = 10
            player.knockback_direction = 1
            player.knockback_direction_y = 0

        if player.last_direction == "up" :
            player.knockback = True
            player.knockback_speed = 10
            player.knockback_direction_y = 1

        if player.last_direction == "down" :
            player.knockback = True
            player.knockback_speed = 10
            player.knockback_direction_y = -1
        player.health_value -= 40
        group.remove(sprite)
    def dead(self, group, sprite):
        smoke = Effect("fumee","frame_",self.rect.centerx, self.rect.centery,(100,100))
        group.add(smoke)
        group.remove(sprite)




