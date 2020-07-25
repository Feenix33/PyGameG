'''
truck.py
'''
import pygame as pg
#import random

from pygame.locals import ( RLEACCEL, )
from direction import Dir

class Truck:
    def __init__(self, clr):
        self.colors = clr

    def create_surface(self):
        surf = pg.Surface(self.owner.wh)
        #surf.set_colorkey(pg.Color("magenta"), RLEACCEL)
        #surf.fill (pg.Color("magenta"))
        surf.fill (pg.Color(self.colors['fill']))
        #pg.draw.rect(surf, pg.Color(self.colors['outline']), self.owner.rect, 2)
        pg.draw.rect(surf, pg.Color(self.colors['outline']), 
                pg.Rect((0,0), self.owner.wh), 1)
        return surf

    def __repr__(self):
        return "Truck"

class AITruck:
    def __init__(self, const, gmap):
        self.gmap = gmap
        self.vel = 0
        self.dim = const['dim']
        self.goal = None
        #self.current = (self.owner.sx / self.dim, self.owner.sy / self.dim) 
        self.current = None
        self.path = None

    def set_goal(self, goal):
        self.goal = goal
        self.current = (self.owner.sx//self.dim, self.owner.sy//self.dim)
        self.path = self.gmap.path(self.current, self.goal)
        self.path.pop(0) # contains the current location

    def step(self):
        if len(self.path) > 0:
            self.current = self.path.pop(0)
            self.owner.sx = self.current[0] * self.dim
            self.owner.sy = self.current[1] * self.dim


    def move(self):
        if self.vel > 0 and self.owner.sx < self.tgtx:
            xvel, yvel = self.owner.direction.xy()
            self.owner.sx += xvel
            #self.owner.sx += self.vel
        else:
            self.vel = 0

    def move2map(self, x, y):
        self.tgtx = self.dim * x
        #self.tgty = self.dim * y
        self.vel = 1

    def __repr__(self):
        response = "dim={} current={} goal={}".format(self.dim, self.current, self.goal)
        response += '\n    path='
        response += str(self.path)
        return response 
