'''
floor.py
'''
import pygame as pg
import random

#gCarpetHeight = 8

class FloorComp:
    def __init__(self, constants, purpose):
        self.purpose = purpose
        self.building = None
        self.carpet_h = constants['carpet_h'] * 2 #double because only half thick is drawn
        self.surface = self.create_surface(constants, purpose)

    def __repr__(self):
        response = "Floor {} {}".format(
                self.purpose,
                self.owner.name,
                )
        return response
        #return "Floor Owner: {} {}".format( repr(self.owner.name), self.owner.ndx,)

    def attach_to_building (building):
        self.building = building

    def create_surface(self, constants, purpose):
        # TODO: Remove hardcoded
        #'wall':'carpet':,'obj1':,'obj2'
        clrs = constants['floor_clrs'][purpose]
        rect = pg.Rect((0,0), constants['floor_wh'])
        surf = pg.Surface((rect.w, rect.h))
        surf.fill (pg.Color(clrs['wall']))
        if purpose == 'com':
            div = random.randrange(4, 10, 2)
            dx = rect.w // div
            ox = dx
            ow = 4
            oh = (rect.h*3)//4
            ot = rect.h - oh
            for _ in range(div//2):
                pg.draw.rect(surf, pg.Color(clrs['obj1']), pg.Rect((ox,ot), (ow, oh)))
                ox += 2*dx
        else:
            objs = random.randrange(2, 4)
            for _ in range(objs):
                clr = random.choice([clrs['obj1'],clrs['obj2'],clrs['obj3']])
                ow = random.randrange(10, 30)
                ox = random.randrange(ow, rect.w-(2*ow))
                oh = random.randrange(rect.h//4, rect.h-(rect.h//4))
                ot = rect.h - oh
                pg.draw.rect(surf, pg.Color(clr), pg.Rect((ox,ot), (ow, oh)))
        pg.draw.line(surf, pg.Color(clrs['carpet']), (0,rect.h), (rect.w, rect.h), self.carpet_h)
        return surf


    @property
    def surf(self):
        return self.surface
