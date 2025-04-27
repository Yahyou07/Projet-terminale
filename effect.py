import pygame

class Effect(pygame.sprite.Sprite):
    def __init__(self,type,name, x, y,scale):
        super().__init__()
        self.images = [pygame.image.load(f"enemy/{type}/{name}{i}.png")for i in range(0,10)]
        self.index = 0
        self.scale = scale
        self.image = self.images[self.index]
        self.image = pygame.transform.scale(self.image,self.scale)
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 0
        

    def update(self, dt):
        self.timer += dt
        if self.timer >= 0.05:  # Vitesse de l'animation (ajuste si besoin)
            self.timer = 0
            self.index += 1
            if self.index < len(self.images):
                self.image = self.images[self.index]
                self.image = pygame.transform.scale(self.image,self.scale)
            else:
                self.kill()  # Supprimer la fumée quand anim terminée
