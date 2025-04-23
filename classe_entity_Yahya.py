import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self,name,x,y):
        super().__init__()
        self.name = name
        self.image = pygame.image.load(f"pnj/{name}/walk/walk1/right1.png")

        self.right_move = [pygame.image.load(f"pnj/{name}/walk/walk1/right{i}.png")for i in range(1,10)]
        self.image = pygame.transform.scale(self.image,(55,55))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.sprite_index = 0
        
    def move_right(self,list_mouv,speed):
        self.rect.x +=1
        self.sprite_index +=speed
        if self.sprite_index >=len(list_mouv):
            self.sprite_index = 0
        self.image = list_mouv[int(self.sprite_index)]

