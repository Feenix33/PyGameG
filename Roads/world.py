'''
world.py
A special entity that doesn't change that much and holds the world information
'''
import pygame as pg

class World:
    def __init__(self, const, gmap 
            ):
        self.dim = const['dim']
        self.w = const['world_width']
        self.h = const['world_height']
        self.color = const['clr_background']
        self.rect = pg.Rect((0,0),(self.w*self.dim, self.h*self.dim))

        self.gmap = gmap
        self.gmap.owner = self

        self._base = pg.Surface((self.w*self.dim, self.h*self.dim))
        self._base.fill (pg.Color(self.color))
        # create drawing surface (same as base for now because no map)
        self._surf = pg.Surface((self.w*self.dim, self.h*self.dim))
        self._surf.fill (pg.Color(self.color))

    def update(self):
        self._surf.blit(self._base, self.rect)
        dim = self.dim
        for x in range(self.w):
            for y in range(self.h):
                if self.gmap.tiles[x][y]:
                    pg.draw.rect(self._surf, pg.Color("blue"), 
                        pg.Rect((x*dim, y*dim),(dim, dim)))

    def draw(self, screen):
        screen.blit(self._surf, self.rect)

    @property
    def surface(self):
        return self._surf

