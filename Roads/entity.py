"""
entity.py
"""

import pygame as pg
from direction import Dir

class Entity:
    _Count = 0
    def __init__(self, name, 
            xy, wh, #xy and wh in pixels
            etype,
            ai=None,
            direction=Dir.R,
            ):
        self.ndx = Entity._Count
        Entity._Count += 1
        self.name = name
        self.etype = etype
        self.wh=wh
        self.rect = pg.Rect(xy, wh)

        self.etype.owner = self
        self._surf = self.etype.create_surface()

        self.ai = ai
        if self.ai: self.ai.owner = self

        self.direction=direction


    def __str__(self):
        return "{:5d} {:10s}: rect({})" \
            .format (self.ndx, self.name, self.rect)

    def __repr__(self):
        response = "{:5d} {:10s} @({},{})".format (self.ndx, self.name, self.sx, self.sy)
        if self.etype:
            response += " etype:{}".format(repr(self.etype))
        if self.ai:
            response += " ai:{}".format(repr(self.ai))
        return response 

    def draw(self, screen):
        screen.blit(self._surf, self.rect)

    @property
    def surface(self):
        return self._surf

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

