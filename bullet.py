import pygame as pg
from pygame.sprite import Sprite

DARK_GRAY = (60,60,60)
SPEED = 5
WIDTH = 3
HEIGHT = 15

class Bullet(Sprite):

    def __init__(self, ai):

        super().__init__()
        self.screen = ai.screen
        self.color = DARK_GRAY

        self.rect = pg.Rect(0,0,WIDTH,HEIGHT)
        self.rect.midtop = ai.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= SPEED
        self.rect.y = self.y

    def draw_bullet(self):
        pg.draw.rect(self.screen, self.color, self.rect)
