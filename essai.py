import pygame

pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 800, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption("Inventaire Drag & Drop")

# Couleurs
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Paramètres de l'inventaire
INV_X, INV_Y = 50, 100
CELL_SIZE = 50
CELL_SIZE2 = 30
CELL_SPACING = 10
INV_COLS = 10
inventory_slots = []

inventory = pygame.image.load("UI/Inventories/barre_outils.png")
# Création des cases d'inventaire (sans affichage)
for i in range(INV_COLS):
    x = INV_X + i * (CELL_SIZE + CELL_SPACING)
    inventory_slots.append(pygame.Rect(x, INV_Y, CELL_SIZE, CELL_SIZE))

# Objets (formes)
objects = [
    {"rect": pygame.Rect(INV_X, INV_Y, CELL_SIZE2, CELL_SIZE2), "shape": "square", "color": RED},
    {"rect": pygame.Rect(INV_X, INV_Y, CELL_SIZE2, CELL_SIZE2), "shape": "square", "color": RED}
    
]
inventaire_postion = [0,0,0,0,0,0]
dragging = None
original_pos = None

running = True
while running:
    screen.fill(WHITE)

    screen.blit(inventory,(-75,60))

    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for obj in objects:
                if obj["rect"].collidepoint(event.pos):
                    dragging = obj
                    original_pos = obj["rect"].center
        elif event.type == pygame.MOUSEBUTTONUP and dragging:
            new_pos = dragging["rect"].center
            valid_slot = None
            
            for slot in inventory_slots:
                if slot.collidepoint(new_pos):
                    occupied = any(o["rect"].colliderect(slot) for o in objects if o != dragging)
                    if not occupied:
                        valid_slot = slot.center
                        break
            
            if valid_slot:
                dragging["rect"].center = valid_slot
            else:
                dragging["rect"].center = original_pos
            
            dragging = None
        elif event.type == pygame.MOUSEMOTION and dragging:
            dragging["rect"].move_ip(event.rel)
    
    # Dessiner les objets
    for obj in objects:
        if obj["shape"] == "square":
            pygame.draw.rect(screen, obj["color"], obj["rect"])
        elif obj["shape"] == "triangle":
            x, y, w, h = obj["rect"]
            pygame.draw.polygon(screen, obj["color"], [(x + w//2, y), (x, y + h), (x + w, y + h)])
    
    pygame.display.flip()

pygame.quit()
