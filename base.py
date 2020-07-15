"""
.py


"""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import random
import pygame as pg


CAPTION = "Title"
SCREEN_SIZE = (400, 400)
MAX_FPS = 30

from pygame.locals import ( RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, \
        QUIT, K_HOME, K_SPACE, K_PAGEUP, K_PAGEDOWN, )



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
                elif event.key == K_SPACE:
                    pass
                elif event.key == K_UP:
                    pass
                elif event.key == K_PAGEUP:
                    pass
                elif event.key == K_PAGEDOWN:
                    pass
                elif event.key == K_DOWN:
                    pass
                elif event.key == K_RIGHT:
                    pass
                elif event.key == K_LEFT:
                    pass
                elif event.key == K_HOME:
                    pass



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
