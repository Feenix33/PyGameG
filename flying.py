"""
flying.py
Fly across changing terrain
arne16
black 000
magenta = 224 111 139
light black = 27 38 50
dark blu 47 72 78

Ship, Clouds, Land all have separate velocities
All have separate update, draw, etc. Try entity system

"""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import random
import pygame as pg


CAPTION = "Flying 01"
SCREEN_SIZE = (800, 500)
MAX_FPS = 20

from pygame.locals import ( RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, \
        QUIT, K_HOME, K_SPACE, K_PAGEUP, K_PAGEDOWN, )

class Ship:
    _limit = 150
    def __init__(self):
        self.bounds = SCREEN_SIZE
        self.image = pg.Surface((50, 20))
        self.image.fill( pg.Color("magenta") )
        self.image.set_colorkey(pg.Color("magenta"), RLEACCEL)

        pg.draw.circle(self.image, pg.Color("yellow3"), (40, 11), 4) # cockpit
        pg.draw.rect(self.image, pg.Color("gray"), pg.Rect((0, 10), (40, 10)) ) # body
        pg.draw.polygon(self.image, pg.Color("gray"), [(0,0),(0,10),(10,10)]) #tail
        pg.draw.polygon(self.image, pg.Color("gray"), [(40,10),(40,20),(50,15)]) # nose
        pg.draw.line(self.image, pg.Color("black"), ( 3,10), ( 8,10), 2) #tail
        pg.draw.line(self.image, pg.Color("black"), (15,15), (30,15), 3) #wings


        self.rect = self.image.get_rect()
        self.rect.left = 200
        self.rect.top = 150
        self.right = True # going right
        self.vel = 5

    def draw(self, surf):
        if self.right:
            surf.blit(self.image, self.rect)
        else:
            surf.blit(pg.transform.flip(self.image, True, False), self.rect)

    def update(self):
        if self.right:
            self.rect.left = self.rect.left - self.vel
            if self.rect.left < Ship._limit:
                self.rect.left = Ship._limit
        else:
            self.rect.left += self.vel
            self.rect.left = min (self.rect.left, self.bounds[0]-Ship._limit)

    def go_left(self): self.right = False
    def go_right(self): self.right = True

class Cloud:
    _rad = 20
    def __init__(self, vel=0):
        self.bounds = SCREEN_SIZE
        if vel==0:
            self.vel = -random.randint(1, 10)/10.
        self.xpos = random.randint(0, self.bounds[0])
        self.image = pg.Surface((Cloud._rad*4, Cloud._rad*3))
        self.image.fill( pg.Color("magenta") )
        self.image.set_colorkey(pg.Color("magenta"), RLEACCEL)
        self.rect = self.image.get_rect()
        clr = pg.Color("whitesmoke")
        pg.draw.circle(self.image, clr, (int(  2*Cloud._rad), int(  2*Cloud._rad)), random.randint(int(0.8*Cloud._rad), int(Cloud._rad)))
        pg.draw.circle(self.image, clr, (int(    Cloud._rad), int(  2*Cloud._rad)), random.randint(int(0.7*Cloud._rad), int(Cloud._rad)))
        pg.draw.circle(self.image, clr, (int(  3*Cloud._rad), int(  2*Cloud._rad)), random.randint(int(0.7*Cloud._rad), int(Cloud._rad)))
        pg.draw.circle(self.image, clr, (int(1.5*Cloud._rad), int(1.5*Cloud._rad)), random.randint(int(0.6*Cloud._rad), int(Cloud._rad)))
        pg.draw.circle(self.image, clr, (int(2.5*Cloud._rad), int(1.5*Cloud._rad)), random.randint(int(0.6*Cloud._rad), int(Cloud._rad)))
        self.rect.top = random.randint(0, self.bounds[1]//4)

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def update(self):
        self.xpos += self.vel
        self.rect.left = int(self.xpos)
        if self.xpos < -100:
            self.xpos = self.bounds[0]+100

class Land:
    def __init__(self):
        self.bounds = SCREEN_SIZE
        self.delta = 20
        midpoint = 3*self.bounds[1] // 4
        minpoint = self.bounds[1]//4
        maxpoint = (7*self.bounds[1])// 8
        self.height = [midpoint]
        #for j in range(self.bounds[0]//self.delta):
        for j in range(80):
            self.height.append(
                min(maxpoint, max(minpoint, self.height[j] + self.delta*random.choice([-1, 0, 0, 1]) )))
        #self.image = pg.Surface((self.delta+self.bounds[0], self.bounds[1]))
        self.image = pg.Surface((self.delta*len(self.height), self.bounds[1]))
        self.image.fill( pg.Color("magenta") )
        self.image.set_colorkey(pg.Color("magenta"), RLEACCEL)
        self.rect = self.image.get_rect()
        self.offset = 0
        self.at = 300
        self.vel = 7
        self.trigger = False
        self.debug = 0

        #draw the screen
        xpos = 0
        n=0
        font = pg.font.SysFont(pg.font.get_default_font(), size=12)
        for ht in self.height:
            seg_rect = pg.Rect(xpos, ht, self.delta, self.bounds[1]-ht)
            if xpos < 20:
                pgclr = "orange"
            elif xpos <= 120:
                pgclr = "brown"
            else:
                pgclr = "forestgreen"
            pg.draw.rect(self.image, pg.Color(pgclr), seg_rect)
            pg.draw.line(self.image, pg.Color("black"), (xpos, ht), (xpos, self.bounds[1]))

            text = font.render(str(n), True, pg.Color("black"))
            self.image.blit(text, (xpos+3, 470))

            xpos += self.delta
            n+=1


    def set_velocity(self, v): self.vel = v
    def change_velocity(self, delta): self.vel += delta

    def draw(self, scrn):
        area = pg.Rect(self.at, 0, self.rect.width-self.at, self.rect.height)
        if self.debug == 0 or self.debug == 1:
            scrn.blit(self.image, (0,0), area)

        dest = (self.rect.width-self.at, 0)
        area.left = 0
        area.width = self.at
        if self.debug == 0 or self.debug == 2:
            scrn.blit(self.image, dest, area)

    def update(self):
        self.at += self.vel
        if self.at > self.rect.width:
            self.at %= self.rect.width
        if self.at < 0:
            self.at += self.rect.width


def hud(surf, land, cloud, ship):
    font = pg.font.SysFont(pg.font.get_default_font(), size=20)
    textclr = "black"

    text = font.render("Vel = "+str(land.vel), True, pg.Color(textclr))
    surf.blit(text, (10, 400))

    text = font.render("Pos = "+str(land.at), True, pg.Color(textclr))
    surf.blit(text, (10, 420))

    outstr = "Pos = {:.0f}".format(cloud.xpos)
    text = font.render(outstr, True, pg.Color(textclr))
    surf.blit(text, (10, 440))

    outstr = "Ship= {}".format(ship.rect.left)
    text = font.render(outstr, True, pg.Color(textclr))
    surf.blit(text, (10, 460))

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)

    pg.key.set_repeat(500, 250)

    screen = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()
    running = True
    earth = Land()
    clouds = []
    for j in range(3):
        clouds.append(Cloud())
    ship = Ship()


    while running:
        for event in pg.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE:
                    earth.trigger = not earth.trigger
                    print(earth.at)
                elif event.key == K_PAGEUP:
                    earth.change_velocity(1)
                elif event.key == K_PAGEDOWN:
                    earth.change_velocity(-1)
                elif event.key == K_HOME:
                    earth.set_velocity(0)
                elif event.key == K_RIGHT:
                    earth.debug = (earth.debug + 1) % 3

            elif event.type == QUIT:
                running = False

        screen.fill(pg.Color("skyblue"))

        # obj.update()
        for cloud in clouds:
            cloud.update()
        if earth.vel < 0:
            ship.go_left()
        else: ship.go_right()
        ship.update()
        earth.update()
            
        # obj.draw(screen)
        for cloud in clouds:
            cloud.draw(screen)
        earth.draw(screen)
        ship.draw(screen)
        hud(screen, earth, clouds[0], ship)


        pg.display.update()
        pg.display.flip()

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
