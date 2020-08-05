"""
FlowField.py
Build a flow field that can interact with the mouse
Have an emitter to generate particles that move to a goal and disappear
TODO:
    how to better do map and world? map is a component of world?
    look at a better map dump routine similar to redgames example

    No check for no path available
    Z-order drawing not implemented
    Magic numbers
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import random
import pygame as pg
#from enum import Enum

#from entity import Entity
from initialize import get_constants
from gamemap import GameMap
from gridworld import GridWorld
from particle import Particle
from goal import Goal
from source import Source

from pygame.locals import ( RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, \
        QUIT, K_HOME, K_SPACE, K_PAGEUP, K_PAGEDOWN, )


def action_system(entities, sources, gmap, world):
    for entity in entities:
        entity.update()

    cleaned =  [entity for entity in entities if entity.alive]

    for source in sources:
        particle_clrs = ["#f94144","#f3722c","#f8961e","#f9844a","#f9c74f","#90be6d","#43aa8b","#4d908e","#577590","#277da1"]

        if source.produce():
            x,y = source.xy
            rad = source.rad -2
            x = x + random.randint(-rad, rad)
            y = y + random.randint(-rad, rad)
            particle = Particle((x,y), (2, 2), 
                    clr=random.choice(particle_clrs),
                    gmap=gmap, world=world)
            cleaned.append(particle)

    return cleaned


def render_system(screen, world, entities):
    # world is slow to change, entities change all the time
    # blit the world to the screen, then draw the entities
    world.draw(screen)
    for entity in entities:
        entity.draw(screen)
    pass


################################################################################
def main():
    #
    # Set up the System
    #
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    constants = get_constants()
    pg.display.set_caption(constants['caption'])
    pg.display.set_mode((constants['screen_width'], constants['screen_height']))

    pg.key.set_repeat(250, 200)

    # screen is the drawing surface
    # display_screen is the screen surface
    # blit the screen to the display with 2x if scaling, else just blit
    screen = pg.Surface ((constants['screen_width'], constants['screen_height']))
    display_screen = pg.display.set_mode ((constants['display_width'], constants['display_height']))

    #font = pg.font.SysFont(pg.font.get_default_font(), size=20)

    clock = pg.time.Clock()
    running = True

    # Create the world
    gmap = GameMap (constants['world_width'], constants['world_height'])
    gmap.make_map()
    dim = constants['dim']
    gx, gy = gmap.goal
    gmap.goal = (gx, gy)


    world = GridWorld(constants, gmap, draw_grid=True)
    world.update() #create the surface
    entities = []
    sources = []

    goal = Goal((gx*dim, gy*dim), (dim, dim), ['orange', 'green'], steps=20)
    entities.append(goal)
    for srcxy in gmap.sources:
        sx, sy = srcxy
        source = Source((sx*dim,sy*dim), (dim, dim),
                steps = 20, slowstep=1)
        entities.append(source)
        sources.append(source)

    #for k, v in constants.items(): print ("{} : {}".format(k, v))


    # inital entity creation
    particle = Particle((100,10), (2, 2), clr="red", gmap=gmap, world=world)
    entities.append(particle)

    action_on = False

    while running:

        for event in pg.event.get():
            pressed = pg.key.get_pressed()

            if event.type == QUIT:
                running = False

            elif event.type == pg.MOUSEBUTTONUP:
                mxy = pg.mouse.get_pos()
                mx, my = mxy
                mx = mx //dim
                my = my //dim
                #print ("MOUSE {} = grid {},{}".format(mxy, mx, my))
                gmap.toggle_tile(mx, my)
                world.update()
                gmap.make_flow()

            elif event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                    running = False
                elif event.key == pg.K_d: #debug
                    print ("Entities = {}".format (len(entities)))
                    for entity in entities:
                        print (repr(entity))

                elif event.key == pg.K_0:
                    pass

                elif pg.K_1 <= event.key <= pg.K_9:
                    pass

                elif event.key == pg.K_g: 
                    world.draw_grid = not world.draw_grid

                elif event.key == pg.K_m: 
                    gmap.dump()

                elif event.key == pg.K_f: 
                    gmap.make_flow()

                elif event.key == pg.K_u: 
                    action_on = not action_on

                elif event.key == pg.K_p: 
                    for source in sources:
                        source.toggle_production()

                else:
                    print ("Key code {} No action".format(event.key))



        #
        # physics system
        #
        if action_on:
           entities = action_system(entities, sources, gmap, world)

        #
        # graphics system
        #
        render_system(screen, world, entities)


        if constants['use_double']:
            pg.transform.scale2x (screen, display_screen)
        else:
            display_screen.blit(screen, screen.get_rect())

        pg.display.update()
        clock.tick_busy_loop(constants['fps'])

    pg.quit()
    sys.exit()

if __name__ == '__main__':
    main()
