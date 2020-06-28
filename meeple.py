"""
meeple.py
First attempt at an ECS system 
A meeple moves from house to office and back again
01 - first ECS attempt and explore
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import random
import pygame as pg
from enum import Enum

CAPTION = "Meeple 01"
GAME_SIZE   = (400, 250)
SCREEN_SIZE = (GAME_SIZE[0]*2, GAME_SIZE[1]*2) #screen is double
MAX_FPS = 30

class RenderOrder(Enum):
    NONE = 0
    BUILDING = 1
    MEEPLE = 2

from pygame.locals import ( RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, \
        QUIT, K_HOME, K_SPACE, K_PAGEUP, K_PAGEDOWN, )

class Entity:
    _Count = 0
    def __init__(self, entities, name, pos, img=None, render=RenderOrder.NONE):
    #def __init__(self, entities, name, rect, img=None):
        self.ndx = Entity._Count
        Entity._Count += 1
        self.name = name
        self.img = img
        self.rect = pg.Rect(pos.x, pos.y, 0, 0)
        self.render_order = render

        if self.img:
            self.img.owner = self
            self.rect = self.img.surf.get_rect()
            self.rect = self.rect.move(pos.x, pos.y)

        entities.append(self)

    def __str__(self):
        #return "    {:5d} {:10s}: p({:3d},{:3d})".format (self.ndx, self.name, self.rect.x, self.rect.y)
        return "    {:5d} {:10s}: {}".format (self.ndx, self.name, self.pos)

    def draw(self, screen):
        screen.blit(self.img.surf, self.rect)

    @property
    def pos(self):
        return Pos(self.rect.x, self.rect.y)

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return "({},{})".format(self.x, self.y)

class MeepleImage:
    def __init__(self, clr):
        self.surf = pg.Surface((10, 20))
        self.surf.fill (clr)
        pg.draw.rect(self.surf, pg.Color("yellow"), pg.Rect((0,0),(10,5)))

class GenericImage40x40:
    def __init__(self, clr):
        self.surf = pg.Surface((40, 40))
        self.surf.fill (clr)

def graphics_system(screen, entities):
    screen.fill(pg.Color("skyblue"))
    pg.draw.rect(screen, pg.Color("gray"), pg.Rect((0, 150), (GAME_SIZE[0],100)))
    for entity in entities:
        entity.draw(screen)
    # demo of alpha, can't draw w/alpha channel
    surf =  pg.Surface((40,40))
    surf.set_alpha(128)
    surf.fill(pg.Color(0,0,255,128))
    screen.blit(surf, pg.Rect((130, 110), (40,40)))

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)

    pg.key.set_repeat(250, 200)

    screen = pg.display.set_mode(SCREEN_SIZE)
    game_screen = pg.Surface(GAME_SIZE)

    font = pg.font.SysFont(pg.font.get_default_font(), size=20)

    clock = pg.time.Clock()
    running = True
    entities = []
    #meeple = Entity(entities, "meeple", pg.Rect((100, 130),(10,20)), 
    meeple = Entity(entities, "meeple", pos=Pos(100,140),
            img=MeepleImage(pg.Color(255,0,0)),
            render=RenderOrder.MEEPLE,
            )

    house = Entity(entities, "house", pos=Pos(20, 110),
            img=GenericImage40x40(pg.Color("blue")),
            render=RenderOrder.BUILDING,
            )

    Entity(entities, "house", pos=Pos(130, 110), img=GenericImage40x40(pg.Color("blue")), render=RenderOrder.BUILDING,)
    Entity(entities, "meeple", pos=Pos(150,130), img=MeepleImage(pg.Color("orange")), render=RenderOrder.MEEPLE,)


    while running:

        for event in pg.event.get():

            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                    running = False
                elif event.key == pg.K_d:
                    #debug
                    for entity in entities:
                        print (entity)

            if event.type == QUIT:
                running = False



        # graphics system
        graphics_system(game_screen, entities)
        #for entity in entities:
        #    entity.draw(game_screen)

        pg.transform.scale2x (game_screen, screen)
        pg.display.update()
        clock.tick_busy_loop(MAX_FPS)

    pg.quit()
    sys.exit()

if __name__ == '__main__':
    main()
