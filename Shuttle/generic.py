'''
generic.py
A generic etype
'''

import pygame as pg
import random

class Generic:
    def __init__(self, clr):
        self.color = clr


    def create_surface(self):
        surf = pg.Surface(self.owner.wh)
        surf.fill (pg.Color(self.color))
        return surf


class DumbAI:
    def __init__(self):
        pass

    def move(self):
        #limit = self.owner.on.h // 2
        #if self.owner.rect.x < limit:
        #    #print (limit, self.owner.rect.x, " ", end="")
        #    self.owner.rect.x += 1
        pass


class BounceAI:
    def __init__(self, vx=0, vy=0):
        self.vx, self.vy = vx,vy
        while self.vx == 0 and self.vy == 0:
            self.vx = random.randint(-3,3)
            self.vy = random.randint(-3,3)

    def move(self):
        wworld,hworld = self.owner.on.wh
        wme, hme = self.owner.wh
        for _ in range(abs(self.vx)):
            self.owner.rect.x += self.vx
            if self.owner.rect.x <= 0:
                self.vx = -self.vx
            elif self.owner.rect.x+wme >= wworld:
                self.vx = -self.vx
                self.owner.rect.x = wworld - wme 

        for _ in range(abs(self.vy)):
            self.owner.rect.y += self.vy
            if self.owner.rect.y <= 0:
                self.vy = -self.vy
            elif self.owner.rect.y+hme >= hworld:
                self.vy = -self.vy
                self.owner.rect.y = hworld - hme 


