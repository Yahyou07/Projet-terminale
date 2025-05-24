import pygame
import numpy as np
def create_gradient_surface(width, height, top_color, bottom_color):
    """Crée une surface avec un dégradé vertical allant de top_color en haut à bottom_color en bas."""
    gradient_surface = pygame.Surface((width, height)).convert_alpha()
    for y in range(height):
        # Calcul d'un ratio allant de 0 (en haut) à 1 (en bas)
        ratio = y / height
        # Interpolation linéaire pour chaque composante RGB
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(gradient_surface, (r, g, b), (0, y), (width, y))
    return gradient_surface

def render_text_gradient_with_outline(text, font, top_color, bottom_color):
    # Rendre le texte blanc avec contour noir
    base_text = font.render(text, True, (255, 255, 255))
    w, h = base_text.get_size()
    outline_surf = pygame.Surface((w + 2, h + 2), pygame.SRCALPHA)

    # Ajoute le contour noir
    outline_size = 3  # ← augmente ce nombre pour un contour plus large
    for dx in range(-outline_size, outline_size + 1):
        for dy in range(-outline_size, outline_size + 1):
            if dx != 0 or dy != 0:
                shadow = font.render(text, True, (82, 51, 63))
                outline_surf.blit(shadow, (dx + outline_size, dy + outline_size))

    # Blit du texte blanc par-dessus le contour
    outline_surf.blit(base_text, (1, 1))

    # Convertir en tableau numpy pour appliquer le dégradé
    arr = pygame.surfarray.pixels3d(outline_surf)
    alpha = pygame.surfarray.pixels_alpha(outline_surf)

    for y in range(h + 2):
        t = y / (h + 1)
        r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
        g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
        b = int(top_color[2] * (1 - t) + bottom_color[2] * t)

        for x in range(w + 2):
            if (arr[x, y] == [255, 255, 255]).all():  # Seulement le texte blanc
                arr[x, y] = [r, g, b]

    return outline_surf.copy()
class Book(pygame.sprite.Sprite):

    def __init__(self,screen):
        super().__init__()

        self.screen = screen
        #définition des polices d'écriture
        self.font = pygame.font.Font("Items/Minecraft.ttf", 14)  # Police par défaut, taille 14
        self.font_book = pygame.font.Font("Font/PixelPurl.ttf", 20)  # Police par défaut, taille 20
        self.font_button_bottom = pygame.font.Font("Font/PixelPurl.ttf", 60)  # Police par défaut, taille 20
        self.font_fantasy = pygame.font.Font("Font/Darinia.TTF", 70)  # Police par défaut, taille 20

        #On charge ici les images des bouttons pour les quete, livre ...
        self.button_book = pygame.image.load("UI/livre2.png")
        self.rect_button_book = self.button_book.get_rect()
        self.rect_button_book.x = self.screen.get_width()-62
        self.rect_button_book.y = 200

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
        
        self.current_book = pygame.transform.scale(self.current_book,(1200,1125))
        self.rect_current_book = self.current_book.get_rect()
        self.rect_current_book.x = 200
        self.rect_current_book.y = -300

        self.IsAnimating = True
        self.IsOpen = False

        self.y_buttons = self.screen.get_height() - 60

        self.button_right_book = pygame.image.load("UI/bouton_droitBook.png")
        self.rect_button_right_book = self.button_right_book.get_rect()
        self.rect_button_right_book.x = 900
        self.rect_button_right_book.y = self.y_buttons

        self.button_left_book = pygame.image.load("UI/bouton_gaucheBook.png")
        self.rect_button_left_book = self.button_left_book.get_rect()
        self.rect_button_left_book.x = 660
        self.rect_button_left_book.y = self.y_buttons
        self.page = 0
        self.page_a_cote = self.page + 1
        self.max_page = 20
        self.pages_text = self.font_fantasy.render(f"{str(self.page)} - {self.page_a_cote}",True, (255, 174, 111))

        self.pages = [render_text_gradient_with_outline("Quest", self.font_fantasy, (255,255,0), (255,165,0))]
        self.pages += [pygame.image.load("UI/barre_title.png") for i in range(self.max_page - 1)]

        self.book_animation_list = []
        self.book_anim_speed = 0
        self.book_anim_index = 0
        self.book_animating = False
        self.Affiche_texte_page = True


    def startBookAnimation(self, liste_mouv, speed):
        self.book_animation_list = liste_mouv
        self.book_anim_speed = speed
        self.book_anim_index = 0
        self.book_animating = True
        self.IsOpen = False
        self.Affiche_texte_page = False   

    def animBook(self):
        if self.book_animating:
            self.book_anim_index += self.book_anim_speed
            if self.book_anim_index >= len(self.book_animation_list):
                self.book_animating = False
                self.IsOpen = True
                self.book_anim_index = len(self.book_animation_list) - 1  # Assurez-vous que l'index est dans les limites
               
                self.Affiche_texte_page = True
            elif self.book_anim_index < 0:
                self.book_anim_index = 0  # Assurez-vous que l'index n'est pas négatif
            self.current_book = self.book_animation_list[int(self.book_anim_index)]
            
            self.current_book = pygame.transform.scale(self.current_book, (1200,1125))  # Appliquez l'échelle ici

    def affiche_book_ui(self):
        # Affichage des bouttons sur le cote
        self.screen.blit(self.button_book,(self.screen.get_width()-80,200))
        pygame.draw.circle(self.screen, (125,125,125), (self.rect_button_book.x+20, self.rect_button_book.y+40), 40,2)
        if self.OnBook:
            self.screen.blit(self.fond_table, (0, 0))
            self.screen.blit(self.current_book, (200, -300))
            self.screen.blit(self.button_back_book, (5, 10))
            

            if self.IsOpen:
                self.screen.blit(self.button_right_book, (900, self.y_buttons))
                self.screen.blit(self.button_left_book, (660, self.y_buttons))
                self.pages_text = self.font_button_bottom.render(f"{str(self.page)} - {self.page_a_cote}",True, (255, 174, 111))
                self.screen.blit(self.pages_text,(760,self.y_buttons + 10))

                if self.Affiche_texte_page:
                    self.screen.blit(self.pages[self.page],(self.rect_current_book.x + 270,self.rect_current_book.y + 452))
                    self.screen.blit(self.pages[self.page_a_cote],(self.rect_current_book.x + 190,self.rect_current_book.y + 520))
                    
    def handle_mouse_event(self,event):
    
        if self.rect_button_book.collidepoint(event.pos):
            show_inventory = False
            self.OnBook = True
            self.startBookAnimation(self.open_book, 0.3)  

        if self.rect_button_back_book.collidepoint(event.pos):
            self.OnBook = False
            moving = True
            self.current_book_index = 0
            self.IsAnimating = True
            self.IsOpen = False

        if self.rect_button_left_book.collidepoint(event.pos) and self.page > 0:
            self.startBookAnimation(self.turn_left, 0.25)
            self.IsOpen = True
            self.page_a_cote = self.page - 1
            self.page -= 2

        if self.rect_button_right_book.collidepoint(event.pos) and self.page < 20:
            self.startBookAnimation(self.turn_right, 0.25)
            self.IsOpen = True
            self.page += 2
            self.page_a_cote = self.page + 1
