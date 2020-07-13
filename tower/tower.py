"""
tower.py
Use an ECS to build a crude Tiny Tower clone

01 - Base outline w/meeple a floor and an elevator
02 - Rethought the ECS
03 - Not working, build a generic graphic E

TODO:
    x Add floor with the construct_floor method
    x shaft
    x add facades

    x build the whole building
    x have res and comm floor in different colors

    x fix the colors dict for floors
    x add random objects in secondary colors for floors
    
    x start elevator
    x move image surf creation into the components, need a generic
    x add elevator placement routines
    x add zorder
    x create ai for elevator to move up and down on timer
    x add doors to elevator; improved drawing routine

    x Rethink how to handle doors for elevator so meeple can wait in front and floor in front meeple

        drawing
    x       base
    x       random
            round heads / transparency
        ai
            moves at random times left and right
            moves to elevator
            calls elevator
            gets on elevator
    elevator 
        ai logic
            get a call up or down
            stop on floor and add passenger
            wait until full during loading
        drawing
            doors open close

    general
        redesign detail surface routines: static, overly, active draw
        elevator needs active with flag
        camera to have taller buildings

    floor
        better random looking floors
            pass in pallet generate: wallpaper, chairs, table, shelves

    building
        add top

    ai ideas for floor:
      res light on/off if people in/out
      comm what items are being sold

"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import random
import pygame as pg
from enum import Enum

from init_tower import get_constants
from entity import Entity

from building import BuildingComp 
from floor import FloorComp
from elevator import ElevatorComp
from ai import ElevatorStates, aiElevator
from meeple import Meeple


from render import render_system, RenderOrder


from pygame.locals import ( RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, \
        QUIT, K_HOME, K_SPACE, K_PAGEUP, K_PAGEDOWN, )

def action_system(entities):
    for entity in entities:
        if entity.ai != None:
            entity.ai.update()

def construct_floor(constants, entities, building, floor_comp):
    top = building.bldgc.top_y
    floor_h = constants['floor_h']
    floor_w = constants['floor_w']
    newtop = top - floor_h
    xpos = 10

    # left facade
    entities.append (Entity ("left facade", pg.Rect((xpos, newtop), (5, floor_h)),
        zorder=RenderOrder.BUILDING, clrs=[constants['bldg2_clrs']['a']], create_surf=True))
    xpos += 5

    # elevator shaft
    entities.append (Entity ("shaft", pg.Rect((xpos, newtop), (30, floor_h)),
        zorder=RenderOrder.BUILDING, clrs=[constants['bldg2_clrs']['b']], create_surf=True))

    xpos += 30


    new_floor = Entity ("floor", pg.Rect((xpos, newtop), (floor_w, floor_h)),
        zorder=RenderOrder.FLOOR, clrs=[], 
        create_surf=False,
        floor_comp=floor_comp)
    entities.append (new_floor)

    xpos += floor_w #take care of the floor

    # right facade
    entities.append (Entity ("right facade", pg.Rect((xpos, newtop), (5, floor_h)),
        zorder=RenderOrder.BUILDING, clrs=[constants['bldg2_clrs']['a']], create_surf=True))


    building.bldgc.add_floor(new_floor)

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    constants = get_constants()
    pg.display.set_caption(constants['caption'])
    pg.display.set_mode((constants['screen_width'], constants['screen_height']))

    pg.key.set_repeat(250, 200)

    background_color = pg.Color(constants['background_color'])

    screen = pg.Surface ((constants['screen_width'], constants['screen_height']))
    display_screen = pg.display.set_mode ((constants['display_width'], constants['display_height']))#(GAME_SIZE)

    font = pg.font.SysFont(pg.font.get_default_font(), size=20)

    clock = pg.time.Clock()
    running = True
    entities = []
    

    # ground 
    entities.append (Entity ("Ground", pg.Rect((0,300),(200,400)), 
            zorder=RenderOrder.BACKGROUND, clrs=["forestgreen"], create_surf=True))

    bldg_comp = BuildingComp(constants)
    building = Entity("Building", 
            rect=pg.Rect(constants['bldg_xy'], constants['bldg_wh']),
            zorder=RenderOrder.BUILDING, clrs=constants['bldg2_clrs'],
            create_surf=False, bldg_comp=bldg_comp)
    entities.append(building)


    construct_floor(constants, entities, building, FloorComp(constants, 'res'))

    # add elevator after a floor has been added
    elev_xy = (constants['elev_x'], building.bldgc.top_y)
    elevator = Entity("Elevator", 
            rect=pg.Rect(elev_xy, constants['elev_wh']),
            zorder=RenderOrder.ELEVATOR, clrs=constants['bldg_clrs'],
            create_surf=False, 
            create_detail=True,
            elev_comp = ElevatorComp(constants),
            ai_comp=aiElevator(constants, building, 0),
            )
    entities.append(elevator)

    construct_floor(constants, entities, building, FloorComp(constants, 'res'))
    construct_floor(constants, entities, building, FloorComp(constants, 'com'))
    construct_floor(constants, entities, building, FloorComp(constants, 'res'))
    construct_floor(constants, entities, building, FloorComp(constants, 'com'))
    construct_floor(constants, entities, building, FloorComp(constants, 'com'))

    # add a meeple
    ypos = building.bldgc.ypos_carpet_on_floor(2) - constants['meep_h']
    xpos = building.bldgc.x4elevator

    ameep =  Entity("Meeple",
            rect=pg.Rect((xpos, ypos), (10,20)),
            zorder=RenderOrder.ELEVATOR, clrs=[],
            create_surf=False, 
            create_detail=False,
            meeple_comp = Meeple(constants),
            )
    entities.append( ameep )
    print("xpos = ", xpos)
    print ("meep @ ", ameep.rect.x)
    print ("floorx ", building.bldgc.floor[1].rect.x )

    while running:

        for event in pg.event.get():
            pressed = pg.key.get_pressed()

            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                    running = False
                elif event.key == pg.K_d: #debug
                    for entity in entities:
                        print (repr(entity))
                elif event.key == pg.K_e: #debug
                        print (repr(elevator))

                elif pg.K_0 <= event.key <= pg.K_9:
                    stop_floor = event.key - pg.K_0
                    elevator.ai.add_stop(stop_floor)


            if event.type == QUIT:
                running = False


        # physics system
        action_system(entities)

        # graphics system
        render_system(screen, entities, background_color)

        pg.transform.scale2x (screen, display_screen)
        pg.display.update()
        clock.tick_busy_loop(constants['fps'])

    pg.quit()
    sys.exit()

if __name__ == '__main__':
    main()
