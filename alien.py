import pygame
from pygame.sprite import Sprite

ACS = 0.5
SPEED = 5



class Alien(Sprite):
    def __init__(self, ai):
        super().__init__()
        self.acs = ACS
        self.speed = SPEED
        self.screen = ai.screen
        self.image = pygame.image.load('images/alien1.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.drop = self.rect.height*1
        self.direction = 1

    def update(self):
        self.x += self.speed *self.direction
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False

