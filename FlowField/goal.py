"""
goal.py
"""

import pygame as pg
#import pygame.gfxdraw
import math
from pygame.locals import (RLEACCEL)

class Goal:
    def __init__(self, 
            xy, wh, #xy and wh in pixels
            clrlist = ['blue', 'yellow'], #color
            steps = 10,
            slowstep=2,
            ):
        self.wh=wh
        self.rect = pg.Rect(xy, wh)
        r = self.rect.width//2
        self._alive = True

        self.surfbank = []
        pi = 3.14159 * 2
        steps = 8
        angle = 0 
        delta = pi / steps
        r2 = r // 2
        for n in range(steps):
            surf = pg.Surface(self.wh)
            #surf.fill (pg.Color('magenta'))
            #surf.set_colorkey (pg.Color('magenta'), RLEACCEL)
            #pg.draw.circle(surf, pg.Color('blue'), (r,r), r)
            surf.fill (pg.Color(clrlist[0]))

            x = int(r+ (0.75*r * math.cos(angle)))
            y = int(r+ (0.75*r * math.sin(angle)))
            angle += delta

            pg.draw.circle(surf, pg.Color(clrlist[1]), (x,y), r2//2)
            self.surfbank.append(surf)

        self.steps = steps
        self.n = steps-1
        self.slowstep = slowstep
        self.slowinc = 0


    def __str__(self):
        response =  "G rect({})".format (self.rect)
        return response 

    def __repr__(self):
        response =  "G rect({}) c{} r{}".format (self.rect, self.rect.center, self.rect.width//2)
        return response 
        return response 

    def update(self):
        pass

    def draw(self, screen):
        #screen.blit(self._surf, self.rect)
        screen.blit(self.surfbank[self.n], self.rect)
        self.slowinc += 1
        if self.slowinc >= self.slowstep:
            self.slowinc = 0
            self.n = (self.n + 1) % self.steps

    def at_goal(self, pt):
        return ((self.rect.left <= pt[0] <= self.rect.right) and \
                (self.rect.top <= pt[1] <= self.rect.bottom))
        
    ### Getters and setters

    @property
    def alive(self):
        return self._alive

    @property
    def w(self): return self.wh[0]

    @property
    def h(self): return self.wh[1]

    @property
    def sx(self): return self.rect.x
    @sx.setter
    def sx(self, sx): self.rect.x = sx

    @property
    def sy(self): return self.rect.y
    @sy.setter
    def sy(self, sy): self.rect.y = sy

