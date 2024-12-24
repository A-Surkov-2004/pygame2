import pygame as pg
from pygame.sprite import Sprite

DARK_GRAY = (60,60,60)
SPEED = 15
WIDTH = 3
HEIGHT = 15
pg.mixer.init()
shot_sound = pg.mixer.Sound('sounds/shot.flac')

class Bullet(Sprite):

    def __init__(self, ai):

        super().__init__()
        self.screen = ai.screen
        self.color = DARK_GRAY

        self.ai = ai

        self.rect = pg.Rect(0,0,WIDTH,HEIGHT)
        self.rect.midtop = ai.ship.rect.midtop
        self.y = float(self.rect.y)
        shot_sound.play()


    def update(self):
        self.y -= SPEED

        self.rect.y = self.y

    def draw_bullet(self):
        pg.draw.rect(self.screen, self.color, self.rect)
