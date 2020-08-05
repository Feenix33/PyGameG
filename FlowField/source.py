"""
source.py
"""

import pygame as pg
import math
from pygame.locals import (RLEACCEL)
import random

class Source:
    def __init__(self, 
            xy, wh, #xy and wh in pixels
            clrlist = ['red', 'black'], #color
            steps = 10,
            slowstep=2,
            ):
        self.wh=wh
        self.rect = pg.Rect(xy, wh)
        self._alive = True
        self.surfbank = []

        # create the images for the surfbank
        side = self.rect.width
        self.steps = steps
        delta = side / (steps)
        for n in range(steps):
            surf = pg.Surface(self.wh)
            surf.fill (pg.Color(clrlist[0]))

            x = int(delta * n)

            pg.draw.line(surf, pg.Color(clrlist[1]), (x,2), (x,side-2), 2)
            self.surfbank.append(surf)

        self.n = random.randint(0, steps-1)
        self.inc = 1
        self.slowstep = slowstep
        self.slowinc = 0
        self.produce_alarm = 10 # when n hits this, create a particle
        self.produce_n = 0
        self.produce_on = False


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
        screen.blit(self.surfbank[self.n], self.rect)
        self.slowinc += 1
        if self.slowinc >= self.slowstep:
            self.slowinc = 0
            self.n = self.n + self.inc
            if self.n == 0: self.inc = -self.inc
            elif self.n >= self.steps:
                self.n = self.steps -1
                self.inc = -self.inc


    def produce(self):
        if not self.produce_on: return
        self.produce_n += 1
        if self.produce_n >= self.produce_alarm:
            self.produce_n = 0
            return True
        return False


    def toggle_production(self):
        self.produce_on = not self.produce_on
        
    ### Getters and setters

    @property
    def alive(self):
        return self._alive

    @property
    def w(self): return self.wh[0]

    @property
    def h(self): return self.wh[1]

    @property
    def rad(self): return self.wh[0]//2  # assumes square

    @property
    def sx(self): return self.rect.x
    @sx.setter
    def sx(self, sx): self.rect.x = sx

    @property
    def sy(self): return self.rect.y
    @sy.setter
    def sy(self, sy): self.rect.y = sy

    @property
    def xy(self): return self.rect.center

