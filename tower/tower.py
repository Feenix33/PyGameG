"""
meeple.py
First attempt at an ECS system 
A meeple moves from house to office and back again
01 - first ECS attempt and explore
02 - refine ECS; pull out meeple and building characteristics

TODO:
x   change entity rect to pos
x   move image creation for building into building
    add a door entity
    add render order building->door->meeple
    add second building
    one building home, other work
    add wait in one then move to other
    meeple inside or outside movement
    building pop
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


from pygame.locals import ( RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, \
        QUIT, K_HOME, K_SPACE, K_PAGEUP, K_PAGEDOWN, )

class MeepleState:
    WAIT = 0
    GO = 1

class Entity:
    _Count = 0
    def __init__(self, entities, name, pos, ground=-1, meeple=None, ai=None, bldg=None):
        self.ndx = Entity._Count
        Entity._Count += 1
        self.name = name
        self.rect = pg.Rect(pos.x, pos.y, 0, 0)
        self.surf = None

        self.meeple = meeple
        self.ai = ai
        self.bldg = bldg

        if self.meeple:
            self.meeple.owner = self
            self.surf = self.meeple.create_surf()
        if self.ai: self.ai.owner = self

        if self.bldg:
            self.bldg.owner = self
            self.surf = self.bldg.create_surf()

        if self.surf:
            self.rect = self.surf.get_rect()
            if ground < 0:
                newy = self.rect.y
            else:
                newy = ground - self.rect.h
            self.rect = self.rect.move(pos.x, newy)
            #print (self.name, self.rect)

        entities.append(self)

    def __str__(self):
        return "    {:5d} {:10s}: {}".format (self.ndx, self.name, self.pos)

    def draw(self, screen):
        screen.blit(self.surf, self.rect)

    @property
    def x(self):
        return self.rect.x
    @property
    def y(self):
        return self.rect.y

    @property
    def pos(self):
        return Pos(self.rect.x, self.rect.y)
    @pos.setter
    def pos(self, x,y):
        self.rect = self.rect.move(x, y)

    def delta_move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return "({},{})".format(self.x, self.y)

class Meeple:
    def __init__(self, clr):
        self.tgtx = 200
        self.clr = clr
    def create_surf(self):
        surf = pg.Surface((10, 20))
        surf.fill (self.clr)
        pg.draw.rect(surf, pg.Color("yellow"), pg.Rect((0,0),(10,5)))
        return surf

class MeepleAI:
    def __init__(self):
        self.state = MeepleState.WAIT
        self.vel = Pos(1,0)
    def move(self):
        actor = self.owner
        #if actor.pos.x < actor.meeple.tgtx:
        if actor.x < actor.meeple.tgtx:
            actor.delta_move(1, 0)


class Door:
    def __init__(self, clr=pg.Color("black")):
        self.clr = clr
    def create_surf(self):
        surf = pg.Surface((10,25))
        surf.set_colorkey(pg.Color("magenta"), RLEACCEL)
        pg.draw.rect(surf, self.clr, pr.Rect((0,0),(10,25)))
        return surf

class Building:
    def __init__(self, clr, w5=8):
        self.clr = clr
        self.population = []
        self.doorx = 0
        self.width = w5*5
    def create_surf(self):
        surf = pg.Surface((self.width, 40))
        surf.fill (self.clr)
        return surf

def graphics_system(screen, entities):
    screen.fill(pg.Color("skyblue"))
    pg.draw.rect(screen, pg.Color("gray"), pg.Rect((0, 150), (GAME_SIZE[0],100)))
    for entity in entities:
        entity.draw(screen)

def action_system(entities):
    for entity in entities:
        if entity.ai:
            entity.ai.move()

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
    #meeple 
    Entity(entities, "meeple", Pos(100,0), ground=150,
            meeple=Meeple(pg.Color("red")), ai=MeepleAI(),
            bldg=None,
            )

    #building
    Entity(entities, "building", Pos(20, 110), ground=150,
            bldg=Building(pg.Color("slategray"), 10),
            )
    Entity(entities, "home", Pos(200, 0), ground=150, bldg=Building(pg.Color("brown"), 20),)


    while running:

        for event in pg.event.get():

            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                    running = False
                elif event.key == pg.K_d: #debug
                    for entity in entities:
                        print (entity)

            if event.type == QUIT:
                running = False


        # physics system
        action_system(entities)

        # graphics system
        graphics_system(game_screen, entities)

        pg.transform.scale2x (game_screen, screen)
        pg.display.update()
        clock.tick_busy_loop(MAX_FPS)

    pg.quit()
    sys.exit()

if __name__ == '__main__':
    main()
