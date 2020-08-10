"""
Routes.py
    Build a distance map and add bugs that randomly follow shortest distances

    Try new technique for the bugs so they only have the x,y in screen coords
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
from drawmap import DrawMapComponent
from bugs import Bugs

from pygame.locals import ( RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, \
        QUIT, K_HOME, K_SPACE, K_PAGEUP, K_PAGEDOWN, )


def action_system(entities):
    for entity in entities:
        entity.action()


def render_system(screen, world, entities):
    world.gc.draw(screen)
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
    world = GameMap (constants['world_width'], constants['world_height'],
            gc = DrawMapComponent (constants),)
    world.make_map()
    world.make_map_from(constants['world_width'], constants['world_height'], constants['world_str'])
    world.set_goal((3, 1))
    world.make_distance_map()


    world.gc.update()
    dim = constants['dim']
    entities = []

    bug_colors = constants['clr_bugs']
    entities.append( Bugs(( 8*dim+dim//2, 5*dim+dim//2), (7, 7),
            clrstr="black", vel=1, dim=dim, world=world,))
    #entities.append( Bugs((16*dim+dim//2, 4*dim+dim//2), (7, 7),
    #        clrstr="blue", vel=3, dim=dim, world=world,))
    entities.append( Bugs(( 8*dim+dim//2, 6*dim+dim//2), (7, 7),
            clrstr=random.choice(bug_colors), vel=1, dim=dim, world=world,))

    # inital entity creation


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
                ok =  world.passable((mx,my))
                #print ("MOUSE {} = grid {},{} is {}".format(mxy, mx, my, ok))
                entities.append( Bugs(mxy, (7, 7),
                    clrstr=random.choice(bug_colors), vel=random.choice([1, 2, 2,3]), dim=dim, world=world,))
                #path = world.build_a_path((mx,my))
                #path.pop() # remove the goal for drawing
                #path.insert(0, (mx,my)) # add the start for drawing
                #print ("PATH  {}".format(path))

            elif event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                    running = False
                elif event.key == pg.K_d: #debug
                    print ("Entities = {}".format (len(entities)))
                    for entity in entities:
                        print (repr(entity))


                elif pg.K_1 <= event.key <= pg.K_9:
                    pass

                elif event.key == pg.K_g: 
                    world.gc.grid = not world.gc.grid 
                    pass

                elif event.key == pg.K_m: 
                    world.dump()
                    world.dump('dist')
                    pass

                elif event.key == pg.K_p: 
                    for entity in entities:
                        entity.toggle_draw_path()

                elif event.key == pg.K_r: 
                    for entity in entities:
                        entity.new_path()

                else:
                    print ("Key code {} No action".format(event.key))



        #
        # physics system
        #
        action_system(entities)
        entities = [entity for entity in entities if entity.alive]

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
