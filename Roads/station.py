'''
station.py

'''
import pygame as pg
#import random

from pygame.locals import ( RLEACCEL, )

class Station:
    def __init__(self, clr):
        self.colors = clr

    def create_surface(self):
        surf = pg.Surface(self.owner.wh)
        #surf.set_colorkey(pg.Color("magenta"), RLEACCEL)
        #surf.fill (pg.Color("magenta"))
        surf.fill (pg.Color(self.colors['fill']))
        #pg.draw.line(surf, pg.Color(self.colors['slash']), (0,0), self.owner.wh, 1)
        #pg.draw.line(surf, pg.Color(self.colors['slash']), (0,self.owner.h), (self.owner.w, 0), 1)
        pg.draw.rect(surf, pg.Color(self.colors['outline']), 
                pg.Rect((0,0), self.owner.wh), 1)


        font = pg.font.SysFont(pg.font.get_default_font(), 3*self.owner.h//2)

        ## fix the rest
        text = font.render(str(self.owner.ndx), False, pg.Color(self.colors['text']))
        surf.blit(text, dest=(self.owner.w//4,0))



        return surf

    def __repr__(self):
        return "Station"

class AIStation:
    def __init__(self, const, gmap):
        self.gmap = gmap

    def move(self):
        pass

    def __repr__(self):
        response = 'AIStation'
        return response 

