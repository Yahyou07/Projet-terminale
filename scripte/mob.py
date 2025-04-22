import pygame

class Mob(pygame.sprite.Sprite):
    def __init__(self, game, x, y,screen):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))  # Fill with red color for visibility
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2
        self.screen = screen

    def distance(self, player):
        """
            Calcule la distance entre le mob et le joueur.
        """
        return ((self.rect.x - player.rect.x) ** 2 + (self.rect.y - player.rect.y) ** 2) ** 0.5
    
    def follow_player(self, player):
        """
            Fait suivre le joueur au mob.
        """
        if self.distance(player) < 50:
            while self.rect.x != player.rect.x:
                if self.rect.x < player.rect.x:
                    self.rect.x += self.speed
                elif self.rect.x > player.rect.x:
                    self.rect.x -= self.speed
            while self.rect.y != player.rect.y:
                if self.rect.y < player.rect.y:
                    self.rect.y += self.speed
                elif self.rect.y > player.rect.y:
                    self.rect.y -= self.speed
            if self.distance(player) == 0:
                self.attack_player(player)

    def attack_player(self, player):
        """
            Fait attaquer le joueur par le mob lorsque la distance est nulle.
        """
        while player.health_value > 0:
            player.health_value -= 1