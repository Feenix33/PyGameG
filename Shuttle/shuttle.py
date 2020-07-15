"""
shuttle.py
Continue to build and ECS
Try surface as a C with recrusive drawing relative to the surface

"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import random
import pygame as pg
from enum import Enum

from initialize import get_constants
from entity import Entity
from generic import Generic, DumbAI, BounceAI

from pygame.locals import ( RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, \
        QUIT, K_HOME, K_SPACE, K_PAGEUP, K_PAGEDOWN, )


def ai_system(screen, entities):
    for entity in entities:
        entity.ai.move()

def render_system(screen, entities):
    for entity in entities:
        entity.draw(screen)


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
    world = Entity("world", (0,0), (constants['screen_width'], constants['screen_height']), etype=Generic("skyblue"))
    entities.append(world)

    #ship = Entity("ship", (70,90), (100,50), etype=Generic("grey"), on=world, ai=DumbAI())
    #ship = Entity("ship", (70,90), (100,50), etype=Generic("grey"), on=world, ai=BounceAI())
    #entities.append(ship)

    #meep = Entity("meep", (10, 10), (5, 5), etype=Generic("yellow"), on=ship, ai=BounceAI())
    #entities.append(meep)
    shipclrs = [ "antiquewhite", "beige", "chocolate", "grey"]
    clrs = ["red","orange","yellow","green","blue","violet"]
    for sclr in shipclrs:
        wx = random.randint(0, 200)
        wy = random.randint(0, 100)
        ww = random.randint(20, 100)
        wh = random.randint(10, 50)
        ship = Entity("ship", (wx,wy), (ww,wh), etype=Generic(sclr), on=world, ai=BounceAI(random.randint(1,2), random.randint(-1,0)))
        entities.append(ship)
        for clr in clrs:
            x = random.randint(0,ww-5)
            y = random.randint(0,wh-5)
            entities.append(
                Entity("meep", (x, y), (5, 5), etype=Generic(clr), on=ship, ai=BounceAI())
            )
    

    while running:

        for event in pg.event.get():
            pressed = pg.key.get_pressed()

            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                    running = False
                elif event.key == pg.K_d: #debug
                    for entity in entities:
                        print (repr(entity))

                elif pg.K_0 <= event.key <= pg.K_4:
                    pass #ship.ai.move()

                elif pg.K_5 <= event.key <= pg.K_9:
                    pass #meep.ai.move()


            if event.type == QUIT:
                running = False


        # physics system
        #action_system(entities)
        for entity in entities:
            if entity.ai:
                entity.ai.move()

        # graphics system
        #render_system(screen, entities)
        world.draw(screen)

        pg.transform.scale2x (screen, display_screen)
        pg.display.update()
        clock.tick_busy_loop(constants['fps'])

    pg.quit()
    sys.exit()

if __name__ == '__main__':
    main()
