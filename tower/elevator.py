'''
elevator.py
        'elev_clrs': {'shell':'outline':'carpet':'c4':'c5':
'''
import pygame as pg
from pygame.locals import ( RLEACCEL )
from ai import ElevatorStates

class ElevatorComp:
    def __init__(self, constants):
        self.surface = self.create_surface(constants)
        self.colors = constants['elev_clrs']

    def __repr__(self):
        response = "Elevator {} {}".format(1, 2)
        if self.owner:
            response += repr(self.owner.ai)
        return response

    def create_surface(self, constants):
        rect = pg.Rect((0,0), constants['elev_wh']) 
        surf = pg.Surface((rect.w, rect.h))
        surf.fill (pg.Color(constants['elev_clrs']['shell']))
        #carpet = constants['elev_carpet']
        #pg.draw.line(surf, pg.Color(carpet), (0,rect.h), (rect.w, rect.h), constants['carpet_h'])
        return surf

    def draw_detail(self, surf):
        surf.fill( pg.Color("magenta") )
        surf.set_colorkey(pg.Color("magenta"), RLEACCEL)
        rect = self.owner.rect
        state = self.owner.ai.state
        if state == ElevatorStates.REST or state == ElevatorStates.MOVE:
            pg.draw.line(surf, pg.Color(self.colors['outline']), (rect.w//2,0), (rect.w//2, rect.h), 2)
        elif state == ElevatorStates.CLOSE:
            pg.draw.rect(surf, pg.Color(self.colors['c4']), pg.Rect((rect.w//4,0), (rect.w//2, rect.h)))
            pg.draw.line(surf, pg.Color(self.colors['carpet']), (0,rect.h), (rect.w, rect.h), 3)
        elif state == ElevatorStates.OPEN or state == ElevatorStates.LOAD:
            pg.draw.rect(surf, pg.Color(self.colors['c5']), pg.Rect((rect.w//4,0), (rect.w//2, rect.h)))
            pg.draw.line(surf, pg.Color(self.colors['carpet']), (0,rect.h), (rect.w, rect.h), 3)


    def attach_to_building (building):
        self.building = building

    @property
    def surf(self):
        return self.surface

