"""
[flying] tiger.py
Fly across changing terrain
First attempt at some commonality
To do:
    HUD works with sliding window
    ship limit based on dimesions
    smooth left right ship movement
    bridges
    trees
    ships
    blow up targets
    ship collision
"""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import random
import pygame as pg


CAPTION = "Flying Tiger"
SCREEN_SIZE = (800, 500)
MAX_FPS = 20

from pygame.locals import ( RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, \
        QUIT, K_HOME, K_SPACE, K_PAGEUP, K_PAGEDOWN, )

class Terrain:
    """ only holds the terrain, no drawing or movement functions """
    def __init__(self, dim=(34, 230), river=(10,34), start=(5,24), bounds=(800,500)):
        self._dim = dim
        self._river = river # min river width, max river width
        self._start = start # len of land, len of river
        self._bounds = bounds
        self._land = [start]

        rmin, rmax = self._river
        #adjust = [-2, -1, -1, 0, 0, 0, 1, 1, 2]
        adjust = [-1, -1, 0, 0, 0, 1, 1]
        for j in range(1,self._dim[1]):
            lshore, river = self._land[j-1]
            ladj = random.choice(adjust)

            river = river - ladj + random.choice(adjust)
            river = max(min(river, rmax), rmin)

            lshore += ladj
            lshore = min(max(lshore, 0), self._dim[0]-rmin)

            while (river + lshore) > self._dim[0]:
                river -= 1
            self._land.append( (lshore, river) )


    def debug(self):
        for line in self._land:
            print (line)
            

class Ship(pg.sprite.Sprite):
    def __init__(self, pos=(0, 0), vel=(0,2), offset=(0,0), dim=(20,20), limit=(34, 230), bounds=(800,500)):
        super(Ship, self).__init__()
        self._pos = pos
        self._dim = dim
        self._bounds = bounds
        self._offset = offset
        self._velocity = vel
        self._tile = 20
        self._limit = limit

        clr = pg.Color("lightgray")
        self._image = pg.Surface(self._dim)
        self._image.fill( pg.Color("magenta") )
        self._image.set_colorkey(pg.Color("magenta"), RLEACCEL)
        pg.draw.polygon( self._image, clr, [(7,20),(13,20),(10,0)])
        pg.draw.polygon( self._image, clr, [(0, 15), (20,15), (10,5) ])
        pg.draw.polygon( self._image, clr, [(5,20), (15,20), (10,10) ])
        clr = pg.Color("goldenrod")
        pg.draw.ellipse( self._image, clr, pg.Rect(8,4,4,8) )
        self._rect = self._image.get_rect()

    def update(self):
        self.fly()

    def move(self, amt):
        self._pos = self._pos[0], min(max((self._pos[1] + amt), 0), 210)

    def fly(self, amt=None):
        if amt is not None:
            velocity = amt
        else:
            velocity = self._velocity
        #self._offset = (self._offset[0] + self._velocity[0], self._offset[1] + self._velocity[1])
        self._offset = (self._offset[0] + velocity[0], self._offset[1] + velocity[1])
        if self._offset[1] >= self._tile:
            self._offset = (self._offset[0], self._offset[1] % self._tile)
            self._pos = (self._pos[0], self._pos[1] + 1)

    def shift(self, amt):
        xoff = self._offset[0]+amt
        posoff = 0
        if abs(xoff) >= self._tile:
            if xoff > 0:
                posoff = 1
                xoff %= self._tile
            else:
                posoff = -1
                xoff = ((xoff+self._tile) % self._tile) - self._tile
            newx = self._pos[0] + posoff
            newx = min(max(0, newx), self._limit[0]-1)
            self._pos = (newx, self._pos[1])

        if (self._pos[0] == 0 and xoff < 0) or (self._pos[0] >= self._limit[0]-1 and xoff > 0):
            xoff = 0
        self._offset = (xoff, self._offset[1]) 

    def accelerate(self, accel):
        vy = self._velocity[1] + accel[1]
        vy = min(max(vy, 2), 10)
        self._velocity = (self._velocity[0], vy)

    def draw(self, screen):
        screen.blit(self._image, self._rect)
    def pos(self): return self._pos
    def offset(self): return self._offset
    def velocity(self): return self._velocity

    def debug(self):
        print ("Position = ", self._pos, ".", self._offset)
        print ("Velocity = ", self._velocity)


def draw_field(screen, land, ship):
    """ prototype drawing the main playing field """
    screen.fill(pg.Color("royalblue"))
    landclr = pg.Color("forestgreen")
    tile = 20
    scrn_rect = screen.get_rect()
    scrn_w, scrn_h = scrn_rect.width, scrn_rect.height
    offset = ship.offset()
    ypos = scrn_h - tile + offset[1]
    n = ship.pos()[1] - 3
    while ypos >= -tile:
        try:
            xlshore = land[n][0] * tile + tile//2
            xrshore = (land[n][0] + land[n][1]) * 20 + tile//2
            wrshore = scrn_w - xrshore
            pg.draw.rect(screen, landclr, pg.Rect(0, ypos, xlshore, tile))
            pg.draw.rect(screen, landclr, pg.Rect(xrshore, ypos, wrshore, tile))
            #pg.draw.line(screen, pg.Color("black"), (0,ypos), (scrn_w, ypos))
            ypos -= tile
            n += 1
        except IndexError:
            print ("Failed at n=", n)
            sys.exit()

    shipx = ship.pos()[0]*tile + (tile//2) + offset[0]
    if shipx < 0:
        print (ship._pos, ship._offset)
    ship_screen = screen.subsurface( pg.Rect(
            shipx, scrn_rect.height-3*tile, tile, tile) )
            #(scrn_rect.width - tile)//2, scrn_rect.height-3*tile, tile, tile) )
    ship.draw(ship_screen)
        

def draw_hud(screen, land, ship):
    """ Rapid draw of the land on the left top to bottom """
    ship_pos = ship.pos()[1]
    lw = 2
    ext = 2
    ypos = (len(land)-1) * lw
    xmax = 35*ext
    scrn_rect = screen.get_rect()
    terraclr = pg.Color("green")
    boundclr = pg.Color("brown")
    riverclr = pg.Color("navy")
    hiltclr = pg.Color("red")
    shipclr = pg.Color("white")
    n = 1
    for shore, river in land:
        pg.draw.line(screen, terraclr, (0, ypos), (shore*ext, ypos), lw)
        if n == 1 or n==len(land):
            pg.draw.line(screen, boundclr, (0, ypos), (shore*ext, ypos), lw)
        n += 1
        pg.draw.line(screen, riverclr, (shore*ext+1, ypos), ((shore+river)*ext, ypos), lw)
        if river >= 35 or river <= 10:
            pg.draw.line(screen, hiltclr, (shore*ext+1, ypos), ((shore+river)*ext, ypos), lw)
        #pg.draw.line(screen, terraclr, ((shore+river)*2+1, ypos), (xmax, ypos), lw)
        lpt = (shore+river)*ext+1
        rpt = xmax
        if lpt < rpt:
            pg.draw.line(screen, terraclr, (lpt, ypos), (rpt, ypos), lw)
        ypos -= lw

    flip_pos = scrn_rect.height - (ship_pos*2) - lw
    pg.draw.line(screen, shipclr, ((scrn_rect.width//2)-1, flip_pos), ((scrn_rect.width//2)+1, flip_pos), lw)


def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)

    pg.key.set_repeat(500, 250)

    screen = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()
    running = True
    #def SHIP(self, pos=(0, 0), offset=(0,0), dim=(20,20), bounds=(800,500)
    ship = Ship(pos=(29,3))


    terra = Terrain()

    while running:
        for event in pg.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE:
                    ship.debug()
                elif event.key == K_UP:
                    ship.accelerate((0,1))
                elif event.key == K_PAGEUP:
                    ship.accelerate((0,10))
                elif event.key == K_PAGEDOWN:
                    ship.accelerate((0,-10))
                elif event.key == K_DOWN:
                    ship.accelerate((0,-1))
                elif event.key == K_RIGHT:
                    ship.shift(5)
                elif event.key == K_LEFT:
                    ship.shift(-9)
                #elif event.key == K_HOME:

            elif event.type == QUIT:
                running = False


        # obj.update()
        ship.update()
            
        # obj.draw(screen)
        screen.fill(pg.Color("skyblue"))
        draw_hud(screen.subsurface(pg.Rect(4,20,70,460)), terra._land, ship)
        draw_field(screen.subsurface(pg.Rect(90,20,700, 460)), terra._land, ship)

        pg.display.flip()
        #pg.display.update() # per docs, update better but need dirty rectangles

        clock.tick_busy_loop(MAX_FPS)

    pg.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()
"""
Code to display a sprite sheet with transparency
    sprite_sheet = pg.image.load("base100x40.png").convert()
    sprite_sheet.set_colorkey(pg.Color(224, 111, 139), RLEACCEL)
    arect = sprite_sheet.get_rect()
"""
