import pygame as pg
import time
COOLDOWN = 0.5
MAX_BULLETS = 3

class Ship():
    def __init__(self, ai):
        self.ai = ai
        self.screen = ai.screen
        self.screen_rect = ai.screen.get_rect()
        self.max_bullets = MAX_BULLETS

        self.image = pg.image.load('images/ship1.PNG')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.lastshot = 0
        self.lives = 3

    def check_cooldown(self):
        if not (time.time() - self.lastshot < COOLDOWN):
            self.lastshot = time.time()
            return True
        else:
            return False

    def blitme(self):
        self.screen.blit(self.image, self.rect)
