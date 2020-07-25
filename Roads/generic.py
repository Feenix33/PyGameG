'''
generic.py
A generic etype
'''

import pygame as pg
import random

from pygame.locals import ( RLEACCEL, )

class Generic:
    def __init__(self, clr):
        self.color = clr

    def create_surface(self):
        surf = pg.Surface(self.owner.wh)
        surf.fill (pg.Color(self.color))
        return surf


class Circle:
    def __init__(self, clr):
        self.color = clr

    def create_surface(self):
        surf = pg.Surface(self.owner.wh)
        center = self.owner.rect.w // 2
        surf.set_colorkey(pg.Color("magenta"), RLEACCEL)
        surf.fill (pg.Color("magenta"))
        pg.draw.circle (surf, pg.Color(self.color), (center,center), center)
        return surf

class Triangle:
    def __init__(self, clr):
        self.color = clr

    def create_surface(self):
        surf = pg.Surface(self.owner.wh)
        surf.set_colorkey(pg.Color("magenta"), RLEACCEL)
        surf.fill (pg.Color("magenta"))

        n = self.owner.rect.w
        h = n // 2
        pg.draw.polygon (surf, pg.Color(self.color), [(h,0),(n,n),(0,n)])
        return surf
