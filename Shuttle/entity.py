"""
entity.py
"""

import pygame as pg

class Entity:
    _Count = 0
    def __init__(self, name, xy, wh, 
            etype,
            on=None,
            ai=None,
            ):
        self.ndx = Entity._Count
        Entity._Count += 1
        self.name = name
        self._basesurf = None
        self.etype = etype
        self.wh=wh
        self.rect = pg.Rect((xy), wh)
        self.on = on
        self.ai = ai
        self.entities = []

        self.etype.owner = self
        self._basesurf = self.etype.create_surface()
        self._surf = pg.Surface(self.wh)

        if ai:
            self.ai.owner = self

        if self.on:
            self.on.entities.append(self)

    def __str__(self):
        return "{:5d} {:10s}: rect({})" \
            .format (self.ndx, self.name, self.rect)

    def __repr__(self):
        response = "{:5d} {:10s}: rect({}) entL={}" \
            .format (self.ndx, self.name, self.rect, len(self.entities))
        return response 

    def draw(self, screen):
        if self._basesurf: 
            self._surf.blit(self._basesurf, pg.Rect((0,0), self.wh))
            for entity in self.entities:
                entity.draw(self._surf)
                #self._surf.blit(entity._surf, entity.rect)
            screen.blit(self._surf, self.rect)

    @property
    def surface(self):
        return self._surf

    @property
    def h(self): return self.wh[1]
