"""
roads.py
ECS Experiment 04
Build a grid map with an entity that follows the path
Add pathfinding AI
- World uses 8x8 tiles and then scaled up to 16x16 in drawing
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import random
import pygame as pg
from enum import Enum

from initialize import get_constants
from entity import Entity
from generic import Generic, Circle, Triangle
from world import World
from gamemap import GameMap
from truck import Truck, AITruck
from station import Station, AIStation

from pygame.locals import ( RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, \
        QUIT, K_HOME, K_SPACE, K_PAGEUP, K_PAGEDOWN, )


def action_system(entities):
    for entity in entities:
        if entity.ai:
            entity.ai.move()
            #pass


def render_system(screen, world, entities):
    world.draw(screen)
    for entity in entities:
        entity.draw(screen)


def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    constants = get_constants()
    pg.display.set_caption(constants['caption'])
    pg.display.set_mode((constants['screen_width'], constants['screen_height']))

    pg.key.set_repeat(250, 200)

    screen = pg.Surface ((constants['screen_width'], constants['screen_height']))
    display_screen = pg.display.set_mode ((constants['display_width'], constants['display_height']))#(GAME_SIZE)

    font = pg.font.SysFont(pg.font.get_default_font(), size=20)

    clock = pg.time.Clock()
    running = True

    gmap = GameMap (constants['world_width'], constants['world_height'])
    gmap.make_map()

    world = World(constants, gmap)
    world.update()

    entities = []
    trucks = []
    stations = []

    dim = constants['dim']

    #truck= Entity("truck", (14*dim,21*dim), (dim, dim), 
    #    etype=Truck(constants['clr_truck']),
    #    ai=AITruck(constants, gmap))
    #entities.append( truck )
    #trucks.append( truck )
    #truck.ai.set_goal((14,21))

    for x,y in gmap.get_trucks_coords():
        truck= Entity("Truck", (x*dim, y*dim), (dim, dim), 
            etype=Truck(constants['clr_truck']),
            ai=AITruck(constants, gmap))
        entities.append( truck )
        trucks.append( truck )
    truck = trucks[0]

    #station= Entity("station", (10*dim,20*dim), (dim, dim), 
    ##    etype=Station(constants['clr_station']),
    #    ai=AIStation(constants, gmap))
    #entities.append( station )
    #stations.append( station )

    for x,y in gmap.get_stations_coords():
        station= Entity("station", (x*dim, y*dim), (dim, dim), 
            etype=Station(constants['clr_station']),
            ai=AIStation(constants, gmap))
        entities.append( station )
        stations.append( station )

    while running:

        for event in pg.event.get():
            pressed = pg.key.get_pressed()

            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                    running = False
                elif event.key == pg.K_d: #debug
                    for entity in entities:
                        print (repr(entity))

                elif event.key == pg.K_0:
                    #truck.ai.step()
                    truck.ai.move()

                #elif event.key == pg.K_1:
                elif pg.K_1 <= event.key <= pg.K_9:
                    sid = event.key - pg.K_1
                    if sid < len(stations):
                        truck.ai.set_goal((stations[sid].sx//dim, stations[sid].sy//dim))
                    pass

                else:
                    print ("Key code {} No action".format(event.key))


            if event.type == QUIT:
                running = False


        # physics system
        action_system(entities)

        # graphics system
        render_system(screen, world, entities)

        pg.transform.scale2x (screen, display_screen)
        pg.display.update()
        clock.tick_busy_loop(constants['fps'])

    pg.quit()
    sys.exit()

if __name__ == '__main__':
    main()
