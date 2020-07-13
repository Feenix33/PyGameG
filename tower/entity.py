"""
entity.py
"""

import pygame as pg

class Entity:
    _Count = 0
    def __init__(self, name, rect, zorder=0, clrs=[], 
            create_surf=True,
            create_detail=False,
            bldg_comp=None,
            floor_comp=None,
            elev_comp=None,
            ai_comp=None,
            meeple_comp=None,
            ):
        self.ndx = Entity._Count
        Entity._Count += 1
        self.name = name
        self.rect = rect
        self.zorder = zorder
        self.surf = None
        if create_surf:
            self.surf = pg.Surface((self.rect.w, self.rect.h))
            self.surf.fill (pg.Color(clrs[0]))

        self.bldgc = bldg_comp
        self.floorc = floor_comp
        self.elevc = elev_comp
        self.ai = ai_comp
        self.meeple = meeple_comp

        self.use_detail = create_detail

        if self.bldgc:
            self.bldgc.owner = self
            self.surf = self.bldgc.surf
            if create_detail:
                self.draw_detail = self.bldgc.draw_detail
        if self.floorc:
            self.floorc.owner = self
            self.surf = self.floorc.surf
            if create_detail:
                self.draw_detail = self.floorc.draw_detail
        if self.elevc:
            self.elevc.owner = self
            self.surf = self.elevc.surf
            if create_detail:
                self.draw_detail = self.elevc.draw_detail

        if self.meeple:
            self.meeple.owner = self
            self.surf = self.meeple.surf

        if self.ai:
            self.ai.owner = self

        if create_detail:
            self.detail_surface = pg.Surface((self.rect.w, self.rect.h))


    def __str__(self):
        return "{:5d} {:10s}: rect({}) z({})" \
            .format (self.ndx, self.name, self.pos, self.zorder)

    def __repr__(self):
        response = "{:5d} {:10s}: rect({}) z({})" \
            .format (self.ndx, self.name, self.pos, self.zorder)
        if self.bldgc != None:
            response += '\n' + '\t' + repr(self.bldgc)
        if self.floorc != None:
            response += '\n' + '\t' + repr(self.floorc)
        if self.ai != None:
            response += '\n' + '\t' + repr(self.ai)
        return response 

    def draw(self, screen):
        if self.surf: 
            screen.blit(self.surf, self.rect)
        if self.use_detail and self.draw_detail:
            self.draw_detail(self.detail_surface)
            screen.blit(self.detail_surface, self.rect)

    @property
    def pos(self):
        return self.rect.x, self.rect.y

    @property
    def py(self):
        return self.rect.y
    @py.setter
    def py(self, y):
        self.rect.y = y

    @property
    def px(self):
        return self.rect.x

