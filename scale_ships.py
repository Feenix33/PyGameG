"""
Scale Ships.py

    Switch entity to use images
    Scaling 2x on the output
    hit counter for score
    Enemy bullets
    different bullets
    Damage not destroy enemies
    Damage not destroy ship
    moving star field in back
    enemy move vertically too
    both bullets w/l/r triggers

To Do:
    sound
    combine torp and bullet management
    health bar on ship
"""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import random
import pygame as pg


CAPTION = "Scale Ships"
SCREEN_SIZE = (800, 500)
GAME_SIZE   = (400, 250)
MAX_FPS = 30
MAX_ENEMIES = 4
MAX_STARS = 20
DMG_BULLET = 110
DMG_TORPEDO = 22
STAR_COLORS = ["gray10", "gray20", "gray30", "gray40", "gray50", "gray60", "gray70", "gray80", "gray90"]
STAR_SIZES = [1, 1, 1, 1, 2, 2, 2, 3]



from pygame.locals import ( RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, \
        QUIT, K_HOME, K_SPACE, K_PAGEUP, K_PAGEDOWN, )



class Entity(pg.sprite.Sprite):
    _Count = 0
    def __init__(self, x, y, img, prefix="E"):
        super(Entity, self).__init__()
        self._name = prefix + str(Entity._Count)
        Entity._Count += 1

        img_rect = img.get_rect()
        self._dim = (img_rect.width, img_rect.height)
        self.image = pg.Surface(self._dim)
        self.image.set_colorkey(pg.Color("magenta"), RLEACCEL)
        self.image.blit(img, img_rect)

        self.rect = self.image.get_rect()
        self.rect.left = int(x)
        self.rect.top = int(y)
        # these are float so we can have non-integer velocities
        self._x = x
        self._y = y

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def debug(self):
        attrs = ['_name', '_x', '_y', 'rect']
        return(', '.join("%s:%s" % (item, getattr(self, item)) for item in attrs))

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, x):
        self._x = x
        self.rect.left = int(self._x)

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, y):
        self._y = y
        self.rect.top = int(self._y)

class Ship(Entity):
    _Fire_Delay = 500
    def __init__(self, x, y, img, prefix="S"):
        super(Ship, self).__init__(x, y, img, prefix)
        self._fire = False
        self._fire_time = 0
        self.alive = True
        self.dead_pos = (-1, -1)
        self._hull = 100
        self._weapon = 0

    def pos_at(self, pos):
        self.x = pos[0] - self._dim[0]//2
        self.y = pos[1] - self._dim[1]//2

    def try_fire(self, weapon=1):
        """ try to fire a weapon if time has passed """
        now = pg.time.get_ticks() 
        if now - self._fire_time < Ship._Fire_Delay: return
        self._fire_time = now
        self._fire = True #fire latch
        self._weapon = weapon

    def weapon_type(self):
        return self._weapon

    def fired(self):
        """ return and reset the fire indicator """
        if self._fire:
            self._fire = False
            return True
        return False

    def get_fire_pos(self):
        x = self.x + self._dim[0]
        y = self.y + self._dim[1] // 2
        return (x, y)

    def take_damage(self, dmg=DMG_TORPEDO):
        self._hull -= dmg
        if self._hull <= 0:
            self.alive = False
            self.dead_pos = (self.x, self.y)

    def is_alive(self):
        return self.alive

    def reset(self):
        self._fire = False
        self.alive = True
        self.dead_pos = (-1, -1)

    def half_width(self):
        return self._dim[1] // 2


class Bullet(Entity):
    def __init__(self, x, y, velocity, prefix="B", dim=(5,1), bounds=None, clr_name="yellow"):
        bullet_image = pg.Surface(dim)
        bullet_image.fill (pg.Color(clr_name))
        super(Bullet, self).__init__(x, y, bullet_image, prefix)
        self._velocity = velocity
        self._bounds = bounds

    def update(self):
        self.x = self.x + self._velocity[0]
        self.y = self.y + self._velocity[1]

    def is_offscreen(self):
        """ just assumes right or left travel """
        offscreen = self._x < -self._dim[0]
        if self._bounds and not offscreen:
            offscreen = self._x > self._bounds.width
        return offscreen



class Enemy(Entity):
    def __init__(self, x, y, img, bounds, yrange=(30,80),prefix="E"):
        super(Enemy, self).__init__(x, y, img, prefix)
        self._velocity = (-3, 0)
        self._bounds = bounds
        #fire control
        self._fired = False
        self._launched = False
        self._timer = 700
        self._start = pg.time.get_ticks() 
        self._hull = 100
        self._yoffset = 0
        self._yrange = random.randrange(yrange[0], yrange[1], 5)
        if self._yrange > 0:
            self._velocity = (self._velocity[0], 1)
            if self.y-self._yrange < 0:
                self.y = self._yrange
            elif self.y+self._yrange > self._bounds.height:
                self.y = self._bounds.height - self._yrange

    def update(self):
        self.x = self.x + self._velocity[0]
        self.y = self.y + self._velocity[1]
        self._yoffset += 1
        if self._yoffset >= self._yrange:
            self._yoffset = 0
            self._velocity = (self._velocity[0], -self._velocity[1])

        if not self._fired:
            now = pg.time.get_ticks() 
            if now - self._start > self._timer:
                self._fired = True #fire latch

    def is_offscreen(self):
        """ just assumes right to left travel """
        return self._x < -self._dim[0]

    def need_launch(self):
        return True if self._fired and not self._launched and self.x < self._bounds.width else False

    def get_fire_pos(self):
        if self._fired and not self._launched:
            x = self.x #+ self._dim[0]
            y = self.y + self._dim[1] // 2
            self._launched = True
            return (x, y)
        return (-100, 0)

    def take_damage(self, dmg=DMG_BULLET):
        self._hull -= dmg
        return True if self._hull <= 0 else False

    def debug(self):
        base = super().debug()
        attrs = [ '_velocity', '_bounds']
        current = ', '.join("%s:%s" % (item, getattr(self, item)) for item in attrs)
        return base + current


class Star(Entity):
    def __init__(self, x, y, rad, bounds, clr_name, prefix="s"):
        star_image = pg.Surface((rad,rad))
        star_image.fill (pg.Color(clr_name))
        super(Star, self).__init__(x, y, star_image, prefix)
        self._velocity = (random.choice([-1,-2,-2,-3,-3,-3,-4]),0)

    def update(self):
        self.x = self.x + self._velocity[0]
        self.y = self.y + self._velocity[1]

    def is_offscreen(self):
        """ just assumes right to left travel """
        return self._x < -self._dim[0]

def star_management(stars, init=False):
    for star in stars:
        if star.is_offscreen():
            stars.remove(star)

    while len(stars.sprites()) < MAX_STARS:
        ypos = random.randrange(20, (SCREEN_SIZE[1]//2)-20, 20)
        xmax = 600 if not init else 800
        xmin = 410 if not init else 0
        xpos = random.randrange(xmin, xmax, 20)
        star_radius = random.choice(STAR_SIZES)
        star_color = random.choice(STAR_COLORS)
        star = Star(x=xpos, y=ypos, rad=star_radius,
                bounds=pg.Rect(0,0,SCREEN_SIZE[0]//2,SCREEN_SIZE[1]//2),
                clr_name=star_color)
        stars.add (star)

def bullet_management(bullets, ship, enemies, entities, effect=None):
    """ check for offscreen bullets, collisions, new bullets """
    shotdown = 0
    for bullet in bullets:
        if bullet.is_offscreen():
            bullets.remove (bullet)
            entities.remove (bullet)

    if len(bullets.sprites()) > 0:
        sprite_dict = pg.sprite.groupcollide(bullets, enemies, True, False)
        if sprite_dict:
            for b, e in sprite_dict.items():
                for bogey in e:
                    if bogey.take_damage():
                        enemies.remove (bogey)
                        entities.remove(bogey)
                        shotdown += 1

    if ship.fired():
        x,y = ship.get_fire_pos()
        if effect: pg.mixer.Channel(0).play(effect)
        if ship.weapon_type() == 1:
            bullet = Bullet(x=x, y=y, velocity=(5,0), dim=(5,5), clr_name="yellow", bounds=pg.Rect(0,0,GAME_SIZE[0],GAME_SIZE[1]))
            bullets.add (bullet)
            entities.add (bullet)
        else:
            offset =  ship.half_width()
            bullet = Bullet(x=x, y=y+offset, velocity=(4,0), dim=(3,3), clr_name="chartreuse", bounds=pg.Rect(0,0,GAME_SIZE[0],GAME_SIZE[1]))
            bullets.add (bullet)
            entities.add (bullet)
            bullet = Bullet(x=x, y=y-offset, velocity=(4,0), dim=(3,3), clr_name="chartreuse", bounds=pg.Rect(0,0,GAME_SIZE[0],GAME_SIZE[1]))
            bullets.add (bullet)
            entities.add (bullet)

    #check if ship collision w/enemy
    collide = pg.sprite.spritecollideany(ship, enemies)
    if collide:
        ship.take_damage()

    return shotdown

def torpedo_management(torps, ship, enemies, entities, effect=None):
    for torp in torps:
        if torp.is_offscreen():
            torps.remove(torp)
            entities.remove(torp)

    if len(torps.sprites()) > 0:
        collide = pg.sprite.spritecollideany(ship, torps)
        if collide:
            ship.take_damage()
            torps.remove (collide)
            entities.remove (collide)

    for enemy in enemies:
        if enemy.need_launch():
            if effect: pg.mixer.Channel(1).play(effect)
            x,y = enemy.get_fire_pos()
            torp = Bullet(x, y, velocity=(-6, 0), prefix="T", clr_name="pink",  dim=(3,1), bounds=pg.Rect(0,0,GAME_SIZE[0],GAME_SIZE[1]))
            torps.add(torp)
            entities.add(torp)

def emeny_management(enemies, entities, img, init=False):
    added = 0
    for bogie in enemies:
        if bogie.is_offscreen():
            enemies.remove (bogie)
            entities.remove (bogie)

    while len(enemies.sprites()) < MAX_ENEMIES:
        ypos = random.randrange(20, (SCREEN_SIZE[1]//2)-20, 20)
        xmax = 600 if not init else 800
        xpos = random.randrange(410, xmax, 20)
        bogie = Enemy(x=xpos, y=ypos, img=img, bounds=pg.Rect(0,0,SCREEN_SIZE[0]//2,SCREEN_SIZE[1]//2))
        enemies.add (bogie)
        entities.add (bogie)
        added += 1

    return added


def draw_boom(surface, pos):
    clrs = [pg.Color("orange"),pg.Color("red"), pg.Color("yellow")]
    x = pos[0]
    y = pos[1]
    
    for _ in range(20):
        pg.draw.circle(surface, 
                random.choice(clrs),
                (x + random.randint(-20, 20), y + random.randint(-20, 30)),
                random.randint(8, 20))

def reset_game(ship, enemies, bullets, entities):
    if ship.is_alive(): return
    ship.reset()
    for enemy in enemies:
        enemies.remove(enemy)
        entities.remove(enemy)
    for bullet in bullets:
        bullets.remove(bullet)
        entities.remove(bullet)

    

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)

    pg.key.set_repeat(250, 200)

    screen = pg.display.set_mode(SCREEN_SIZE)
    game_screen = pg.Surface((SCREEN_SIZE[0]//2,SCREEN_SIZE[1]//2))

    font = pg.font.SysFont(pg.font.get_default_font(), size=20)

    clock = pg.time.Clock()
    running = True

    entities = pg.sprite.Group()
    bullets = pg.sprite.Group()
    enemies = pg.sprite.Group()
    torps = pg.sprite.Group()
    stars = pg.sprite.Group()
    enemy_count = 0
    shot_down = 0

    effect = pg.mixer.Sound('..\\assets\\laser03.wav')
    #pg.mixer.Channel(0).play(pg.mixer.Sound('..\\assets\\laser03.wav'))
    effect2 = pg.mixer.Sound('..\\assets\\laser04.wav')

    ship = Ship (x=20, y=100, img=pg.image.load('spaceship20x20.png'))
    entities.add (ship)

    enemy_img = pg.image.load('spaceshipB20x20.png')
    enemy_count = emeny_management(enemies, entities, enemy_img, init=True)

    star_management(stars, init=True)

    while running:
        for event in pg.event.get():

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT: pass
                if event.key == pg.K_LEFT: pass
                if event.key == pg.K_SPACE:
                    reset_game(ship, enemies, bullets, entities)
                    enemy_count = 0
                    shot_down = 0
                if event.key == pg.K_q:
                    running = False
                if event.key == pg.K_c:
                    # print sprite group counts
                    print ("entities={} enemies={} bullets={} ship={}".format(
                        len(entities.sprites()), len(enemies.sprites()), len(bullets.sprites()),1))
                if event.key == pg.K_e:
                    # print debugs for entities
                    for e in entities:
                        print(e.debug())
                if event.key == pg.K_f: pass
                if event.key == pg.K_t:
                    print (bogie.is_offscreen())
                if event.key == pg.K_m:
                    print ('mouse=',pg.mouse.get_pos())

                if event.key == pg.K_ESCAPE: 
                    running = False

            if event.type == pg.KEYUP: pass

            #if event.type == pg.MOUSEBUTTONDOWN:
            #    ship.try_fire()

            if event.type == QUIT:
                running = False


        #screen.fill(pg.Color("black"))
        game_screen.fill(pg.Color("black"))

        if ship.is_alive():
            # mouse ship interaction
            mx,my = pg.mouse.get_pos()
            mx,my = mx//2, my//2
            ship.pos_at((mx,my))

            if pg.mouse.get_pressed()[0]:
                ship.try_fire(1)
            elif pg.mouse.get_pressed()[2]:
                ship.try_fire(2)


            stars.update()
            entities.update()
            star_management(stars)
            enemy_count += emeny_management(enemies, entities, enemy_img)
            shot_down += bullet_management(bullets, ship, enemies, entities, effect)
            torpedo_management(torps, ship, enemies, entities, effect2)


        stars.draw(game_screen)
        entities.draw(game_screen)

        # end game overlay
        if not ship.is_alive():
            draw_boom(game_screen, ship.dead_pos)

        # status bar
        status_text = "Enemies={:3d} Shot={:3d} {:5s}".format(
                enemy_count, shot_down, str(ship.is_alive()))
        game_screen.blit (font.render(status_text, False, pg.Color("white")), (0,0))


        pg.transform.scale2x (game_screen, screen)
        pg.display.update()
        clock.tick_busy_loop(MAX_FPS)

    pg.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()
