import pickle
import random
import sys
import time

import powerup
from ship import Ship
import pygame
import pygame as pg
from bullet import Bullet
from alien import Alien

HEIGHT = 1080
WIDTH = 1920
LIGHT_GRAY = (200, 200, 200)
SPEED = 16
FPS = 60
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PW_RATE = 10
PW_TIME = 5


pg.mixer.init()
boom_sound = pg.mixer.Sound('sounds/boom.flac')
gameover_sound = pg.mixer.Sound('sounds/gameover.wav')
lvlup_sound = pg.mixer.Sound('sounds/lvlup.wav')
powerup_sound = pg.mixer.Sound('sounds/powerup.wav')




class AlienInvasion:
    def __init__(self):
        self.raytime = 0
        self.ray = False
        self.lvl = 1
        pg.init()
        self.lstpw = time.time()
        self.running = True
        self.width = WIDTH
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        self.bg_color = LIGHT_GRAY
        self.ship = Ship(self)
        self.clock = pygame.time.Clock()
        self.bullets = pg.sprite.Group()
        self.aliens = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self._create_fleet()
        self.powerup_types = []
        self.pu = None
        self.powerup_types.append(powerup.Heal_powerup)
        self.powerup_types.append(powerup.Ray_powerup)
        pg.display.set_caption('Alien Invasion')

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self._check_events()
            if self.ship.lives != 0 and len(self.aliens) != 0:
                self.bullets.update()
                self._update_aliens()
            self.next_lvl_check()
            self._update_powerups()
            self._update_screen()
            self._remove_bullets()

    def _check_events(self):

        print(self.raytime - time.time())

        if not self.ray:
            if self.raytime > time.time():
                self.ray = True
        elif self.raytime - time.time() < 0:
            self.ray = False

        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] and self.ship.rect.x < WIDTH - self.ship.rect.size[0]:
            self.ship.rect.x += SPEED

        if keys[pg.K_LEFT] and self.ship.rect.x > 0:
            self.ship.rect.x -= SPEED

        if keys[pg.K_SPACE] and self.ship.check_cooldown():
            self._fire_bullet()

        for event in pg.event.get():
            if event.type == pygame.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q):
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    self.save_game()
                if event.key == pg.K_l:
                    self.load_game()


    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.powerups.draw(self.screen)
        self.display_UI()
        pg.display.flip()

    def _fire_bullet(self):
        if len(self.bullets) < self.ship.max_bullets or self.ray:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _remove_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        collisions = pg.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if len(collisions) != 0:
            boom_sound.play()
            for i in self.aliens:
                i.speed += i.acs

    def _create_fleet(self):
        alien = Alien(self)
        aw, ah = alien.rect.size
        avspace = WIDTH - 2 * alien.rect.width
        number_ali = avspace // (2 * alien.rect.width)
        ship_h = self.ship.rect.height
        avspace_y = (HEIGHT - (3 * ah) - ship_h)
        rows = avspace_y // (2 * ah)

        for j in range(rows):
            for i in range(number_ali):
                self._create_alien(i, j)

    def _create_alien(self, number, row):
        alien = Alien(self)
        aw, ah = alien.rect.size
        alien.x = aw + 2 * aw * number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row
        self.aliens.add(alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        collisions = pg.sprite.spritecollide(self.ship, self.aliens, True)
        if len(collisions) != 0:

            self.ship.lives -= 1
            if self.ship.lives == 0:
                gameover_sound.play()
                self.ship.rect.y = HEIGHT + self.ship.rect.height
            boom_sound.play()

    def _update_powerups(self):
        for i in self.powerups:
            if time.time() - i.spawntime > PW_TIME:
                self.pu.kill()
                self.powerups.remove()
        if self.lstpw + PW_RATE < time.time():
            self.lstpw = time.time()
            self.pu = random.choice(self.powerup_types)(self)
            self.powerups.add(self.pu)

        collisions = pg.sprite.groupcollide(self.bullets, self.powerups, True, False)

        if len(collisions) != 0:
            powerup_sound.play()
            self.pu.activate()
            self.pu.kill()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                alien.rect.y += alien.drop
                alien.direction *= -1

    def display_UI(self):
        f1size = 50
        f1 = pygame.font.Font(None, f1size)
        f2 = pygame.font.Font(None, 100)
        text1 = f1.render(f'Ships: {self.ship.lives}', True,
                          RED)
        self.screen.blit(text1, (0, 0))

        text1 = f1.render(f'Level: {self.lvl}', True,
                          RED)
        self.screen.blit(text1, (0, f1size))

        if self.ship.lives == 0:
            text1 = f2.render(f'GAME OVER!', True,
                              RED)
            self.screen.blit(text1, (WIDTH / 3, HEIGHT / 3))

    def next_lvl_check(self):
        if len(self.aliens) == 0:
            self.lvl += 1
            self._create_fleet()
            lvlup_sound.play()

    def save_game(self):
        data = (self.lvl, self.ship.lives)
        filename = "savefile.pkl"
        with open(filename, "wb") as f:
            pickle.dump(data, f)

    def load_game(self):
        filename = "savefile.pkl"
        with open(filename, "rb") as f:
            data = pickle.load(f)

        for i in self.aliens:
            i.kill()

        self.ship.lives = data[1]
        self.lvl = data[0]

        self._create_fleet()

        print(data)


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run()
