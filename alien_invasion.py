import sys
from ship import Ship
import pygame
import pygame as pg
from bullet import Bullet
from alien import Alien


HEIGHT = 1080
WIDTH = 1920
LIGHT_GRAY = (200,200,200)
SPEED = 16
FPS = 60
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class AlienInvasion:
    def __init__(self):
        pg.init()
        self.running = True
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        self.bg_color = LIGHT_GRAY
        self.ship = Ship(self)
        self.clock = pygame.time.Clock()
        self.bullets = pg.sprite.Group()
        self.aliens = pg.sprite.Group()
        self._create_fleet()
        pg.display.set_caption('Alien Invasion')


    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self._check_events()
            if self.ship.lives != 0 and len(self.aliens) != 0:
                self.bullets.update()
                self._update_aliens()
            self._update_screen()
            self._remove_bullets()






    def _check_events(self):

        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] and self.ship.rect.x < WIDTH-self.ship.rect.size[0]:
            self.ship.rect.x += SPEED

        if keys[pg.K_LEFT] and self.ship.rect.x > 0:
            self.ship.rect.x -= SPEED

        if keys[pg.K_SPACE] and self.ship.check_cooldown():
            self._fire_bullet()



        for event in pg.event.get():
            if event.type == pygame.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q):
                self.running = False


    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.display_UI()
        pg.display.flip()

    def _fire_bullet(self):
        if(len(self.bullets) < self.ship.max_bullets):
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _remove_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        collisions = pg.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if len(collisions) != 0:
            for i in self.aliens:
                i.speed += i.acs


    def _create_fleet(self):
        alien = Alien(self)
        aw, ah = alien.rect.size
        avspace = WIDTH - 2 * alien.rect.width
        number_ali = avspace // (2 * alien.rect.width)
        ship_h = self.ship.rect.height
        avspace_y = (HEIGHT - (3*ah)-ship_h)
        rows = avspace_y // (2*ah)

        for j in range(rows):
            for i in range(number_ali):
                self._create_alien(i, j)

    def _create_alien(self, number, row):
        alien = Alien(self)
        aw, ah = alien.rect.size
        alien.x = aw + 2*aw*number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row
        self.aliens.add(alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        collisions = pg.sprite.spritecollide(self.ship, self.aliens, True)
        if len(collisions) != 0:
            self.ship.lives -= 1


    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                alien.rect.y += alien.drop
                alien.direction *= -1

    def display_UI(self):
        f1 = pygame.font.Font(None, 100)
        text1 = f1.render(f'Ships: {self.ship.lives}', True,
                          RED)
        self.screen.blit(text1, (0, 0))

        if self.ship.lives == 0:
            text1 = f1.render(f'GAME OVER!', True,
                              RED)
            self.screen.blit(text1, (WIDTH/3, HEIGHT/3))
        if len(self.aliens) == 0:
            text1 = f1.render(f'YOU ARE VICTORIOUS!', True,
                              GREEN)
            self.screen.blit(text1, (WIDTH/3, HEIGHT/3))





if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run()
