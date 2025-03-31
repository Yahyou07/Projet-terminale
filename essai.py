import pygame

pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 800, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Inventaire Drag & Drop")

# Couleurs
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
YELLOW = (255,255,0)
# Paramètres de l'inventaire
INV_X = 50
INV_Y = 100
CELL_SIZE = 50
CELL_SPACING = 10
INV_COLS = 10

inventory_slots = []
inventory_state = [0] * INV_COLS  # Liste de suivi des emplacements

inventory = pygame.image.load("UI/Inventories/barre_outils.png")

# Création des cases d'inventaire
for i in range(INV_COLS):
    x = INV_X + i * (CELL_SIZE + CELL_SPACING)
    inventory_slots.append(pygame.Rect(x, INV_Y, CELL_SIZE, CELL_SIZE))

square_img = pygame.image.load("Items/apple_icon.png")

# Objets (formes)
objects = [
    {"rect": pygame.Rect(INV_X, INV_Y, CELL_SIZE, CELL_SIZE), "image": square_img, "slot": None}
]

# Centrer l'objet par défaut dans la première case
objects[0]["rect"].center = inventory_slots[0].center
inventory_state[0] = 1
objects[0]["slot"] = 0

dragging = None
original_pos = None

running = True
while running:
    screen.fill(WHITE)
    screen.blit(inventory, (23, 60))

    # Dessiner les cases d'inventaire
    for i, slot in enumerate(inventory_slots):
        pygame.draw.rect(screen, GRAY, slot, 2)
        if inventory_state[i] == 1:
            pygame.draw.rect(screen, YELLOW, slot, 2)  # Mettre en évidence les cases occupées

    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for obj in objects:
                if obj["rect"].collidepoint(event.pos):
                    dragging = obj
                    original_pos = obj["rect"].center
                    if obj["slot"] is not None:
                        inventory_state[obj["slot"]] = 0  # Libérer l'ancien slot
                        obj["slot"] = None
        elif event.type == pygame.MOUSEBUTTONUP and dragging:
            new_pos = dragging["rect"].center
            valid_slot = None
            
            for i, slot in enumerate(inventory_slots):
                if slot.collidepoint(new_pos) and inventory_state[i] == 0:
                    valid_slot = i
                    break
            
            if valid_slot is not None:
                dragging["rect"].center = inventory_slots[valid_slot].center
                inventory_state[valid_slot] = 1
                dragging["slot"] = valid_slot
            else:
                dragging["rect"].center = original_pos
            
            dragging = None
        elif event.type == pygame.MOUSEMOTION and dragging:
            dragging["rect"].move_ip(event.rel)
    
    # Dessiner les objets
    for obj in objects:
        obj_x = obj["rect"].centerx - obj["image"].get_width() // 2
        obj_y = obj["rect"].centery - obj["image"].get_height() // 2
        screen.blit(obj["image"], (obj_x, obj_y))
    
    pygame.display.flip()
    print(inventory_state)  # Affichage de l'état des slots dans la console

pygame.quit()
