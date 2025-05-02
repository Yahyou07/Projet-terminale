import pygame
import sys
 
pygame.init()
 
# Constantes
WIDTH, HEIGHT = 600, 400
FONT = pygame.font.SysFont("arial", 24)
TITLE_FONT = pygame.font.SysFont("arial", 36)
BG_COLOR = (245, 245, 245)
TEXT_COLOR = (0, 0, 0)
ACTIVE_COLOR = (30, 144, 255)
INACTIVE_COLOR = (200, 200, 200)
BUTTON_COLOR = (100, 200, 100)
BUTTON_HOVER_COLOR = (80, 180, 80)
BUTTON_TEXT_COLOR = (255, 255, 255)
 
# Fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connexion")
 
# Champs de texte
class InputBox:
    def __init__(self, x, y, w, h, is_password=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = INACTIVE_COLOR
        self.text = ""
        self.txt_surface = FONT.render("", True, TEXT_COLOR)
        self.active = False
        self.is_password = is_password

        self.cursor_visible = True
        self.cursor_counter = 0
        
    def update_cursor(self):
        if self.active:
            self.cursor_counter += 1
            if self.cursor_counter >= 5:  # Change toutes les ~500 ms à 60 FPS
                self.cursor_visible = not self.cursor_visible
                self.cursor_counter = 0
        else:
            self.cursor_visible = False
            self.cursor_counter = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                if self.cursor_position > 0:
                    self.text = self.text[:self.cursor_position - 1] + self.text[self.cursor_position:]
                    self.cursor_position -= 1
            elif event.key == pygame.K_DELETE:
                if self.cursor_position < len(self.text):
                    self.text = self.text[:self.cursor_position] + self.text[self.cursor_position + 1:]
            elif event.key == pygame.K_LEFT:
                if self.cursor_position > 0:
                    self.cursor_position -= 1
            elif event.key == pygame.K_RIGHT:
                if self.cursor_position < len(self.text):
                    self.cursor_position += 1
            elif event.key == pygame.K_RETURN:
                pass
            else:
                self.text = self.text[:self.cursor_position] + event.unicode + self.text[self.cursor_position:]
                self.cursor_position += 1

            self.update_text_surface()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = ACTIVE_COLOR if self.active else INACTIVE_COLOR
            if self.active:
                # Calcul de la position du curseur cliqué
                relative_x = event.pos[0] - (self.rect.x + 5)
                self.cursor_position = len(self.text)
                for i in range(len(self.text) + 1):
                    sub_text = "*" * i if self.is_password else self.text[:i]
                    width = FONT.size(sub_text)[0]
                    if width >= relative_x:
                        self.cursor_position = i
                        break
 
    def update_text_surface(self):
        display_text = "*" * len(self.text) if self.is_password else self.text
        self.txt_surface = FONT.render(display_text, True, TEXT_COLOR)

        
 
    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y))
        #pygame.draw.rect(screen, self.color, self.rect, 1)
        if self.active and self.cursor_visible:
            display_text = "*" * self.cursor_position if self.is_password else self.text[:self.cursor_position]
            cursor_x = self.rect.x + 5 + FONT.size(display_text)[0]
            cursor_y = self.rect.y
            cursor_height = self.txt_surface.get_height()
            pygame.draw.line(screen, TEXT_COLOR, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)

        
 
# Bouton
class Button:
    def __init__(self, x, y, w, h, text, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.hovered = False
 
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()
 
    def update(self):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
 
    def draw(self, screen):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect)
        text_surface = FONT.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)