import pygame
class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed=300, range_px=100):
        super().__init__()
        self.image = pygame.Surface((16, 4))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))

        self.direction = direction
        self.speed = speed
        self.range_px = range_px
        self.distance_travelled = 0

    def update(self):
        # Utilise dt globalement
        global dt
        dx, dy = 0, 0
        if self.direction == "up":
            dy = -1
        elif self.direction == "down":
            dy = 1
        elif self.direction == "left":
            dx = -1
        elif self.direction == "right":
            dx = 1

        move_x = dx * self.speed * dt
        move_y = dy * self.speed * dt

        self.rect.x += move_x
        self.rect.y += move_y

        self.distance_travelled += abs(move_x) + abs(move_y)
        if self.distance_travelled >= self.range_px:
            self.kill()
