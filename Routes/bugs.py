"""
bugs.py
"""

import pygame as pg
import random

class Bugs:
    _Count = 0
    def __init__(self, 
            xy, wh,
            clrstr="black",
            vel=1,
            dim=1,
            world=None,
            ):
        self.ndx = Bugs._Count
        Bugs._Count += 1
        self._rect = pg.Rect((0,0), wh)
        self.pgclr = pg.Color(clrstr)
        self.vel = vel
        self.dim = dim
        self.world = world

        self._surf = pg.Surface(self._rect.size)
        self._surf.fill (self.pgclr)
        self._alive = True
        self._rect.center = xy
        gx = self._rect.centerx // self.dim
        gy = self._rect.centery // self.dim
        self.path = self.world.build_a_path((gx,gy))
        self.screen_path = []
        self.build_screen_path()
        self.draw_path = False #debug only, comment out test in draw routine

    def __str__(self):
        return "B{:05d} at ({})" \
            .format (self.ndx, self._rect.center)

    def __repr__(self):
        response = "P{:05d} rect({}) at ({}) vel={} size={}" \
            .format (self.ndx, self._rect, self._rect.center, self.vel, self._rect.size)
        response += "  on world ({}) ".format((self._rect.centerx//self.dim, self._rect.centery//self.dim))
        response += "\n    path = [{}]".format(self.path)
        return response 

    def action(self):
        if not self._alive: return
        for _ in range(self.vel):
            if not self.screen_path:
                self._alive = False
                return
            tgtx, tgty = self.screen_path[0]
            vx, vy = 0, 0
            #dist = abs(tgtx - self.x) + abs(tgty - self.y)
            if tgtx > self.x: vx = 1
            elif tgtx < self.x: vx = -1
            if tgty > self.y: vy = 1
            elif tgty < self.y: vy = -1
            self.x += vx
            self.y += vy
            if vx != 0 and vy != 0:
                if random.random() > 0.5: vx = 0
                else: vy = 0
            if self._rect.center == self.screen_path[0]:
                del self.screen_path[0]

    def draw(self, screen):
        if not self._alive: return
        screen.blit(self._surf, self._rect)
        if not self.draw_path: return
        if self.screen_path and len(self.screen_path) >= 2:
            pg.draw.lines(screen, pg.Color("yellow"), False, self.screen_path, 2)
        if self.screen_path:
            pg.draw.line(screen, pg.Color("pink"), self._rect.center, self.screen_path[0], 2)

    def build_screen_path(self):
        self.screen_path = []
        half = self.dim // 2
        rlo = self.dim // 4
        rhi = self.dim - rlo
        for x,y in self.path:
            sx = x*self.dim
            sy = y*self.dim
            sx += random.randint(rlo, rhi)
            sy += random.randint(rlo, rhi)
            self.screen_path.append((sx, sy))

    def new_path(self):
        gx = self._rect.centerx // self.dim
        gy = self._rect.centery // self.dim
        self.path = self.world.build_a_path((gx,gy))
        self.build_screen_path()


    def toggle_draw_path(self):
        self.draw_path = not self.draw_path

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
    def w(self): return self._rect.width

    @property
    def h(self): return self._rect.height

    @property
    def x(self): return self._rect.centerx
    @x.setter
    def x(self, x): self._rect.centerx = x

    @property
    def y(self): return self._rect.centery
    @y.setter
    def y(self, y): self._rect.centery = y

