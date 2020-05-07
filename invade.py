"""
invade.py
simplistic shooter


To Do:
    OR convert bullets to add delete sprite?
    x and y properties should do modulo on reverses
    use actual sprites
    mask collisions
    use invader group velocity?
    add invader return fire
"""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import random
import pygame as pg


CAPTION = "Invaders"
SCREEN_SIZE = (800, 500)
MAX_FPS = 30
MAX_BULLETS = 10
BULLET_DELAY = 500  # msec to wait between bullets
RETURN_FIRE = 100 # times out of 1000 that an enemy returns fire


from pygame.locals import ( RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, \
        QUIT, K_HOME, K_SPACE, K_PAGEUP, K_PAGEDOWN, )

class Entity(pg.sprite.Sprite):
    _Count = 0
    def __init__(self, x, y, prefix="E", alive=True, dim=(20,20), bounds=None):
        super(Entity, self).__init__()
        self._x = x
        self._y = y
        self._alive = alive
        self._dim = dim
        if bounds is None:
            self._bounds = pg.Rect((0,0), (SCREEN_SIZE[0]-dim[0], SCREEN_SIZE[1]-dim[1])) 
        else:
            self._bounds = bounds 
        self.image = pg.Surface(self._dim)
        self.rect = self.image.get_rect()
        self.rect.left = self._x
        self.rect.top = self._y
        self._name = prefix + str(Entity._Count)
        Entity._Count += 1

    def update(self):
        pass

    def draw(self, screen):
        if self._alive:
            screen.blit(self.image, self.rect)

    def debug(self, suppress=False):
        if suppress:
            print (self._name, self._alive, self._x, self._y, self._bounds, end="", flush=True)
        else:
            print (self._name, self._alive, self._x, self._y, self._bounds, type(self._bounds))
        pass

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, x):
        self._x = min(max(x, self._bounds.left), self._bounds.right)
        self.rect.left = int(self.x)

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, y):
        self._y = min(max(y, self._bounds.top), self._bounds.bottom)
        self.rect.top = int(self.y)

class Player(Entity):
    _fire_delay = 0
    def __init__(self, x, y, prefix="Play", alive=True, dim=(20,10), bounds=pg.Rect((0,0), SCREEN_SIZE)):
        super(Player, self).__init__(x, y, prefix, alive, dim, bounds)
        self.image.fill( pg.Color("magenta") )
        self.image.fill( pg.Color("green") )
        self.image.set_colorkey(pg.Color("magenta"), RLEACCEL)
        #safety
        self.y += 0
        self.x += 0
        self._velocity = (0,0)
        self._bullets = []

    def attach_bullets(self, bullets):
        self._bullets = bullets

    def fire_bullet(self):
        now = pg.time.get_ticks() 
        if now - Player._fire_delay < BULLET_DELAY: return
        Player._fire_delay = now
        for bullet in self._bullets:
            if bullet.alive == False:
                bullet.launch(self._x+self._dim[0]//2, self._y)
                break

    def move(self, speed):
        self.x += speed

    def accelerate(self, accel):
        self._velocity = (self._velocity[0] + accel[0],self._velocity[1] + accel[1])

    #def draw(self, screen):
    #    super().draw(screen)

    def debug(self):
        super().debug(True)
        print (" v=", self._velocity)
        for bullet in self._bullets:
            print ("---- ", end="")
            bullet.debug()

    @property
    def velocity(self):
        return self._velocity
    @velocity.setter
    def velocity(self, velocity):
        self._velocity = velocity

    def update(self):
        if not self._alive: return
        self.x += self.velocity[0]
        self.y += self.velocity[1]

class Bullet(Entity):
    def __init__(self, x, y, prefix="Bull", alive=False, dim=(2,10), bounds=pg.Rect((0,0), SCREEN_SIZE), clr_name="yellow", velocity=(0,-4)):
        super(Bullet, self).__init__(x, y, prefix, alive, dim, bounds)
        self.image.fill (pg.Color(clr_name))
        self._velocity = velocity
        self._alive = False

    def launch(self, x, y):
        self._alive = True
        self.x = x
        self.y = y

    def update(self):
        if self._alive:
            self.x += self._velocity[0]
            self.y += self._velocity[1]
            #todo change to rect bottom
            #if self.y <= 0:
            if self.y <= self._bounds.top or self.y >= self._bounds.bottom:
                self._alive = False

    #def draw(self, screen):
    #    if self._alive:
    #        screen.blit(self.image, self.rect)

    @property
    def alive(self):
        return self._alive
    @alive.setter
    def alive(self, value):
        self._alive = value


class Invader(Entity):
    _Fleet_reverse = False # signal to all invaders to reverse
    def __init__(self, x, y, prefix="Invd", alive=True, dim=(20,15), bounds=pg.Rect((0,0), SCREEN_SIZE)):
        super(Invader, self).__init__(x, y, prefix, alive, dim, bounds)
        self.image.fill( pg.Color("magenta") )
        self.image.fill( pg.Color("red") )
        self.image.set_colorkey(pg.Color("magenta"), RLEACCEL)
        self._velocity = (0,0)


    def change_color(self, clr_name="white"):
        self.image.fill( pg.Color(clr_name) )

    def update(self):
        if not self._alive: return
        self.x += self._velocity[0]
        self.y += self._velocity[1]

    def reverse(self):
        self._velocity = (-self._velocity[0], self._velocity[1])
        self.y += self.rect.height//2

    def fleet_signal(self):
        return Invader._Fleet_reverse

    def fleet_reset(self, value=False):
        Invader._Fleet_reverse = value

    def draw(self, screen):
        super().draw(screen)

    @property
    def x(self):
        #return self._x
        return super().x
    @x.setter
    def x(self, x):
        self._x = x
        if self._x <= self._bounds.left or self._x >= self._bounds.right:
            self._x = min(max(x, self._bounds.left), self._bounds.right)
            Invader._Fleet_reverse = True
        self.rect.left = int(self.x)

    @property
    def velocity(self):
        return self._velocity
    @velocity.setter
    def velocity(self, velocity):
        self._velocity = velocity


def create_invaders(invaders, entities, start, spacing, cols, rows, row_spacing):
    ypos = start[1]
    iwidth = SCREEN_SIZE[0]-25-2*start[0]
    for _ in range(rows):
        xpos = start[0]
        for _ in range (cols):
            invader = Invader(x=xpos, y=ypos, dim=(25,15), bounds=pg.Rect((25*2,0), (iwidth, SCREEN_SIZE[1])))
            invader.velocity = (-0.5, 0)
            invaders.add(invader)
            entities.add (invader)
            xpos += spacing
            if xpos > iwidth:
                break
        ypos -= row_spacing
        if ypos < 0:
            break

    invader = random.choice(invaders.sprites())
    invader.change_color(clr_name="white")

def create_random_bird(invaders, entities, birds):
    """ have a confirm launch of a bird, pick a random invader"""
    bullet = Bullet(0, 0, clr_name="hotpink", velocity=(0,1))
    invader = random.choice(invaders.sprites())
    bullet.launch(invader.x+invader._dim[0]//2, invader.y)
    birds.add (bullet)
    entities.add (bullet)


def clean_birds(entities, birds):
    for bird in birds:
        if not bird.alive:
            birds.remove (bird)
            entities.remove (bird)



def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)

    pg.key.set_repeat(250, 200)

    screen = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()
    running = True

    entities = pg.sprite.Group()

    player = Player(x=100, y=SCREEN_SIZE[1]-100) #, bounds=pg.Rect((100,0),(400,900)))
    entities.add (player)

    bullets = pg.sprite.Group()
    birds = pg.sprite.Group()

    for _ in range(MAX_BULLETS):
        bullet = Bullet(0, 0, clr_name="blue", velocity=(0,-10))
        bullets.add (bullet)
        entities.add (bullet)

    player.attach_bullets(bullets)

    #invaders = []
    invaders = pg.sprite.Group()
    invader_start_y = 150
    create_invaders(invaders, entities, (50,150), 50, 10, 4, 30)


    while running:
        for event in pg.event.get():

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    player.velocity = (3,0)
                if event.key == pg.K_LEFT:
                    player.velocity = (-3,0)
                if event.key == pg.K_ESCAPE:
                    running = False
                if event.key == pg.K_SPACE:
                    player.fire_bullet()
                    #print (pg.time.get_ticks())

                if event.key == pg.K_s:
                    player.debug()
                if event.key == pg.K_i:
                    for i in invaders: i.debug()
                if event.key == pg.K_q:
                    running = False
                if event.key == pg.K_e:
                    for e in entities:
                        e.debug()
                if event.key == pg.K_f:
                    create_random_bird(invaders, entities, birds)
                if event.key == pg.K_c:
                    print ('Counts e({}) i({}) b({}) '.format( 
                            len(entities.sprites()),
                            len(invaders.sprites()),
                            len(birds.sprites()),
                            ))
                if event.key == pg.K_m:
                    r = pg.Rect((50,20), (30, 40))
                    print (r)
                    print (r.left, r.right)

            if event.type == pg.KEYUP:
                # should rework for if both are down and only one lifted
                if event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
                    player.velocity = (0,0)

            if event.type == QUIT:
                running = False


        screen.fill(pg.Color("black"))

        entities.update()
        for bullet in bullets:
            if bullet.alive:
                hits = pg.sprite.spritecollide(bullet, invaders, True)
                if hits:
                    bullet.alive = False

        clean_birds(entities, birds)

        if Invader._Fleet_reverse:
            for invader in invaders:
                invader.reverse()
            Invader._Fleet_reverse = False

        if not len(invaders.sprites()):
            invader_start_y +=  50
            create_invaders(invaders, entities, (50,invader_start_y), 50, 10, 4, 30)
            for bullet in bullets:
                bullet.alive = False

        for entity in entities:
            entity.draw(screen) #so we can use the alive flag in the blit
        #entities.draw(screen)

        pg.display.flip()
        clock.tick_busy_loop(MAX_FPS)

    pg.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()
