"""
particle.py
"""

import pygame as pg
import random

class Particle:
    _Count = 0
    def __init__(self, 
            xy, wh, #xy and wh in pixels
            clr, #color
            vel=1,
            gmap=None,
            world=None,
            ):
        self.ndx = Particle._Count
        Particle._Count += 1
        self.wh=wh
        self.rect = pg.Rect(xy, wh)
        self.pgclr = pg.Color(clr)
        self.vel = vel

        self._surf = pg.Surface(self.wh)
        self._surf.fill (self.pgclr)
        self.gmap = gmap
        self.world = world
        self._alive = True

        self.prev_vel = (0, 0)
        self.turn_count = 0


    def __str__(self):
        return "P{:5d} rect({})" \
            .format (self.ndx, self.rect)

    def __repr__(self):
        response = "P{:5d} rect({}) vel={}" \
            .format (self.ndx, self.rect, self.vel)
        gx, gy = self.world.screen2grid(self.rect.topleft)
        response += " grid=({},{})".format(gx, gy)
        response += " flow=({})".format(self.gmap.flow[gx][gy])
        return response 

    def update(self):
        if not self._alive: return

        #gx, gy = self.world.screen2grid(self.rect.topleft)
        gx, gy = self.world.screen2grid(self.rect.center)
        vx, vy = self.gmap.flow[gx][gy]
        if self.prev_vel != (vx, vy):
            if self.turn_count < 0:
                self.turn_count = random.randint(2, 38) #magic numbers need dim to be passed
            else:
                self.turn_count -= 1
            if self.turn_count == 0:
                self.turn_count = -1
                self.prev_vel = (vx, vy)
            else:
                vx, vy = self.prev_vel


        self.rect.left += vx
        self.rect.top += vy
        if (gx, gy) == self.gmap.goal:
            self._alive = False

    def draw(self, screen):
        if not self._alive: return
        screen.blit(self._surf, self.rect)

    ###################################
    ### Getters and setters
    ###################################

    @property
    def alive(self):
        return self._alive

    @property
    def surface(self):
        return self._surf

    @property
    def w(self): return self.wh[0]

    @property
    def h(self): return self.wh[1]

    @property
    def sx(self): return self.rect.x
    @sx.setter
    def sx(self, sx): self.rect.x = sx

    @property
    def sy(self): return self.rect.y
    @sy.setter
    def sy(self, sy): self.rect.y = sy

