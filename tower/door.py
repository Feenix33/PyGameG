'''
door.py
    door for elevators
'''
import pygame as pg
from pygame.locals import ( RLEACCEL )

class Door:
    def __init__(self, constants, building, floor):
        self.surface = self.create_surface(constants)
        self.colors = constants['door_clrs']
        self.building = building
        self.floor = floor

    def __repr__(self):
        response = "Elevator {} {}".format(1, 2)
        if self.owner:
            response += repr(self.owner.name)
        return response

    def create_surface(self, constants):
        rect = pg.Rect((0,0), constants['door_wh']) 
        surf = pg.Surface((rect.w, rect.h))
        surf.fill (pg.Color(constants['door_clrs']['shell']))
        return surf

    def draw_detail(self, surf):
        surf.fill( pg.Color("magenta") )
        surf.set_colorkey(pg.Color("magenta"), RLEACCEL)
        rect = self.owner.rect
        pg.draw.rect(surf, pg.Color(self.colors['c5']), pg.Rect((rect.w//4,0), (rect.w//2, rect.h)))
        pg.draw.line(surf, pg.Color(self.colors['carpet']), (0,rect.h), (rect.w, rect.h), 3)




    @property
    def surf(self):
        return self.surface

