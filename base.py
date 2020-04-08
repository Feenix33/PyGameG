"""
.py
Simple bouncing balls using pygame

"""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import random
import pygame as pg


CAPTION = "Bounce 04"
SCREEN_SIZE = (400, 400)
MAX_FPS = 30

from pygame.locals import ( K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT,)



def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)

    screen = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()
    running = True

    while running:
        for event in pg.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            elif event.type == QUIT:
                running = False

        screen.fill(pg.Color("black"))

        # obj.update()
            
        # obj.draw(screen)


        pg.display.update()
        pg.display.flip()

        clock.tick_busy_loop(MAX_FPS)

    pg.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()
