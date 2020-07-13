import pygame as pg

class BuildingComp:
    def __init__(self, constants):
        self.floor = []
        self.shafts = []
        self.elevs = []
        self.floor_h = constants['floor_h']
        self.floor_x = constants['floor_x']
        self.surface = self.create_surface(constants)
        self.carpet_offset = constants['floor_carpet_off']
        self.carpet_h = constants['carpet_h']
        self.meeple_h = constants['meep_h']

    def __repr__(self):
        response =  "Building Owner: {} {}".format(
                repr(self.owner.name),
                self.owner.ndx,
                )
        if len(self.floor) > 0:
            for floor in self.floor:
                response += "\n\t" + repr(floor)
        return response

    def add_floor(self, floor):
        self.floor.append(floor)

    def create_surface(self, constants):
        clrs = constants['bldg2_clrs']
        # hardcoding the values
        rect=pg.Rect(constants['bldg_xy'], constants['bldg_wh'])
        surf = pg.Surface((rect.w, rect.h))
        surf.fill (pg.Color(clrs['a']))
        pg.draw.rect(surf, pg.Color(clrs['b']), pg.Rect((rect.w/2-30, rect.h-30), (60, 30)))
        pg.draw.rect(surf, pg.Color(clrs['c']), pg.Rect((rect.w/2-30, rect.h-30), (60, 30)), 1)
        pg.draw.rect(surf, pg.Color(clrs['c']), pg.Rect((0,0), (rect.w-1, rect.h-1)), 2)
        return surf

    def floor2ypos(self, floor_num):
        return self.owner.rect.y - self.floor_h * (floor_num + 1)

    def ypos_carpet_on_floor(self, floor_num):
        return self.owner.rect.y - self.floor_h * (floor_num) - self.carpet_h + 1


    @property
    def nfloors(self): #where is the top of the building
        return len(self.floor) -1

    @property
    def top_y(self): #where is the top of the building
        return self.owner.rect.y - self.floor_h*len(self.floor)

    @property
    def y4top(self): #where is the top of the building
        return self.owner.rect.y - self.floor_h*len(self.floor)

    @property
    def surf(self):
        return self.surface

    @property
    def x4elevator(self):
        return self.floor_x

