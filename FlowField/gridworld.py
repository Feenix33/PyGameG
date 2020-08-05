'''
GridWorld.py
'''
import pygame as pg

class GridWorld:
    def __init__(self, const, gmap,
            draw_grid=False,
            ):
        self.dim = const['dim']
        self.w = const['world_width']
        self.h = const['world_height']
        self.color = const['clr_world_background']
        self.rect = pg.Rect((0,0),(self.w*self.dim, self.h*self.dim))
        self.clr_tiles = const['clr_world']
        self.clr_grid = const['clr_world_grid']
        self._draw_grid = draw_grid
        self.clr_goal = const['clr_world_goal']
        self.clr_source = const['clr_world_source']

        self.gmap = gmap
        self.gmap.owner = self

        self._base = pg.Surface((self.w*self.dim, self.h*self.dim))
        self._base.fill (pg.Color(self.color))
        # create drawing surface (same as base for now because no map)
        self._surf = pg.Surface((self.w*self.dim, self.h*self.dim))
        self._surf.fill (pg.Color(self.color))

    def update(self):
        '''
        TODO: Make this more generic
        '''
        self._surf.blit(self._base, self.rect)
        dim = self.dim
        for x in range(self.w):
            for y in range(self.h):
                if self.gmap.tiles[x][y]:
                    pg.draw.rect(self._surf, pg.Color(self.clr_tiles[self.gmap.tiles[x][y]]),
                        pg.Rect((x*dim, y*dim),(dim, dim)))

        if self.gmap.goal:
            x, y = self.gmap.goal
            pg.draw.rect(self._surf, pg.Color(self.clr_goal), pg.Rect((x*dim, y*dim),(dim, dim)))
        for source in self.gmap._sources:
            x, y = source
            pg.draw.rect(self._surf, pg.Color(self.clr_source), pg.Rect((x*dim, y*dim),(dim, dim)))


        if self._draw_grid:
            for x in range(self.w):
                for y in range(self.h):
                    pg.draw.rect(self._surf, pg.Color(self.clr_grid), pg.Rect((x*dim, y*dim),(dim, dim)), 1)

    def draw(self, screen):
        screen.blit(self._surf, self.rect)

    def screen2grid(self, pt):
        x,y = pt
        gx = x // self.dim
        gy = y // self.dim
        return (gx, gy)

    def grid2screen(self, pt):
        x,y = pt
        sx = x * self.dim
        sy = y * self.dim
        return (sx, sy)


    @property
    def surface(self):
        return self._surf

    @property
    def draw_grid(self):
        return self._draw_grid
    @draw_grid.setter
    def draw_grid(self, dg):
        self._draw_grid = dg
        self.update()
