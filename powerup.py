import random
import time

import pygame
from pygame.sprite import Sprite

RAY_TIME = 2

class Base_powerup(Sprite):
    def __init__(self, ai):
        super().__init__()
        self.ai = ai
        self.screen = ai.screen
        self.spawntime = time.time()





    def activate(self):
        pass


class Heal_powerup(Base_powerup):
    def __init__(self, ai):
        super().__init__(ai)
        self.image = pygame.image.load('images/heal.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = random.random()*ai.width % (ai.width-self.rect.width)
        self.rect.y = self.rect.height

    def activate(self):
        self.ai.ship.lives += 1

class Ray_powerup(Base_powerup):
    def __init__(self, ai):
        super().__init__(ai)
        self.image = pygame.image.load('images/ray.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = random.random() * ai.width % (ai.width - self.rect.width)
        self.rect.y = self.rect.height

    def activate(self):
        self.ai.raytime = time.time() + RAY_TIME



