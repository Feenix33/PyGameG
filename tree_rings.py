"""
tree.py
Draw tree rings
"""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import random
import pygame as pg


CAPTION = "Tree Rings 01"
SCREEN_SIZE = (800, 500)
MAX_FPS = 20

from pygame.locals import ( K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT,)


def draw_rings1(screen):
    def ring(numPts, rad, off):
        # generate the points and return as a list of pairs
        points = []
        pt = pg.Vector2()
        shifted = pg.Vector2()
        angle = 0
        angle_delta = 360.0 / numPts

        for j in range(numPts):
            pt.from_polar((rad, angle))
            shifted = pt + off
            points.append((int(shifted.x), int(shifted.y)))
            angle += angle_delta

        return points


    screen.fill(pg.Color("tan"))
    ring_delta = 8
    ring_radius = ring_delta
    num_points = 6
    ring_points = []
    num_rings = 10
    ring_width = random.randint(2, 5)
    center = screen.get_rect().center

    for nr in range(num_rings):
        ring_points = ring(num_points, ring_radius, center)
        pt0 = ring_points[-1]
        for pt in ring_points:
            pg.draw.line(screen, pg.Color("black"), pt0, pt, ring_width)
            pt0 = pt
        ring_radius += ring_width + random.randint(ring_delta//2, ring_delta*4//3)
        num_points *= 2


def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)

    screen = pg.display.set_mode(SCREEN_SIZE)
    center = pg.Vector2()
    center = (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2)
    clock = pg.time.Clock()
    running = True

    once = True

    while running:
        for event in pg.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            elif event.type == QUIT:
                running = False

        if once:
            draw_rings1(screen)
            once = False

    
        # obj.update()
            
        # obj.draw(screen)


        pg.display.update()
        pg.display.flip()

        clock.tick_busy_loop(MAX_FPS)

    pg.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()
