'''
DrawMap.py
    This is a component to separate it from the gamemap routines 
'''
import pygame as pg

class DrawMapComponent:
    def __init__(self, const,
            ):
        self.dim = const['dim']
        self.world_width = const['world_width']
        self.world_height = const['world_height']
        self.screen_width = const['screen_width']
        self.screen_height = const['screen_height']
        self._grid = False

        self.color_bank = const['clr_world']
        

        self.rect = pg.Rect((0,0),(self.screen_width, self.screen_height))


        self._base = pg.Surface((self.screen_width, self.screen_height))
        self._base.fill (pg.Color(self.color_bank['background']))

        self._surf = pg.Surface((self.screen_width, self.screen_height))
        #self._surf.fill (pg.Color(self.color_bank['background']))
        #self.update()


    def update(self):
        self._surf.blit(self._base, self.rect)
        #if self._grid:
        #    gridclr = pg.Color(self.color_bank['grid'])
        #    for x in range(0, self.screen_width, self.dim):
        #        for y in range(0, self.screen_height, self.dim):
        #            rect = pg.Rect((x,y), (self.dim, self.dim))
        #            pg.draw.rect(self._surf, gridclr, rect, 1)
#
        sx = 0
        gridclr = pg.Color(self.color_bank['grid'])
        wallclr = pg.Color(self.color_bank['wall'])
        goalclr = pg.Color(self.color_bank['goal'])
        for x in range(self.world_width):
            sy = 0
            for y in range(self.world_height):
                rect = pg.Rect((sx,sy), (self.dim, self.dim))
                if (x,y) == self.owner.goal:
                    pg.draw.rect(self._surf, goalclr, rect)
                elif self.owner.tiles[x][y] !=  1:
                    pg.draw.rect(self._surf, wallclr, rect)
                if self._grid:
                    pg.draw.rect(self._surf, gridclr, rect, 1)
                sy += self.dim
            sx += self.dim

    def draw(self, screen):
        screen.blit(self._surf, self.rect)

    @property
    def surface(self):
        return self._surf

    @property
    def grid(self):
        return self._grid
    @grid.setter
    def grid(self, dg):
        self._grid = dg
        self.update()
