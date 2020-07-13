import random
import pygame as pg

class Meeple:
    def __init__(self, constants):
        self.surface = self.create_surface(constants)

    def create_surface(self, constants):
        clr_jeans = random.choice(constants['meep_jeans'])
        clr_hair = random.choice(constants['meep_hair'])
        clr_face = random.choice(constants['meep_face'])
        clr_shirt = random.choice(constants['meep_shirt'])
        #print (clr_jeans, clr_hair, clr_face, clr_shirt)

        surf = pg.Surface((constants['meep_w'], constants['meep_h']))
        surf.fill (pg.Color(clr_jeans))

        rect = pg.Rect((0, 0), (constants['meep_w'], constants['meep_hhair']))
        pg.draw.rect(surf, pg.Color(clr_hair), rect)

        rect.top = rect.top + constants['meep_hhair']
        rect.height = constants['meep_hface']
        pg.draw.rect(surf, pg.Color(clr_face), rect)

        rect.top = rect.top + constants['meep_hface']
        rect.height = constants['meep_hshirt']
        pg.draw.rect(surf, pg.Color(clr_shirt), rect)
        return surf

    @property
    def surf(self):
        return self.surface

