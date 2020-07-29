'''
truck.py

'''
import pygame as pg
#import random

from pygame.locals import ( RLEACCEL, )
from direction import Dir


class Truck:
    def __init__(self, clr):
        self.colors = clr

    def create_surface(self):
        surf = pg.Surface(self.owner.wh)
        #surf.set_colorkey(pg.Color("magenta"), RLEACCEL)
        #surf.fill (pg.Color("magenta"))
        surf.fill (pg.Color(self.colors['fill']))
        #pg.draw.rect(surf, pg.Color(self.colors['outline']), self.owner.rect, 2)
        pg.draw.rect(surf, pg.Color(self.colors['outline']), 
                pg.Rect((0,0), self.owner.wh), 1)
        return surf

    def __repr__(self):
        return "Truck"

class AITruck:
    def __init__(self, const, gmap):
        self.gmap = gmap
        self.velocity = 5
        self.velocity = 1
        self.dim = const['dim']
        self.goal = None
        self.goal_queue = []
        #self.current = (self.owner.sx / self.dim, self.owner.sy / self.dim) 
        self.current = None
        self.path = []

    def set_goal(self, goal):
        self.goal_queue.append(goal)
        #self.build_path_to_goal()

    def build_path_to_goal(self):
        if not self.goal_queue: return # no goals to set

        self.goal = self.goal_queue.pop(0)
        self.current = (self.owner.sx//self.dim, self.owner.sy//self.dim)
        self.path = self.gmap.path(self.current, self.goal)
        if len(self.path): # possible no path exists
            self.path.pop(0) # contains the current location
        else:
            print ("ERROR: No path")

    def step(self):
        if len(self.path) > 0:
            self.current = self.path.pop(0)
            self.owner.sx = self.current[0] * self.dim
            self.owner.sy = self.current[1] * self.dim


    def move(self):
        if len(self.path) == 0: 
            if self.goal_queue:
                self.build_path_to_goal()
            return
        for _ in range(self.velocity):
            self.move_one_increment()

    def move_one_increment(self):
        if len(self.path) == 0: return

        dbgpopped = False
        dbgtop = False

        goal = self.path[0]
        vx, vy = 0,0
        if self.current[0] == goal[0]: # vel is y
            dbgtop = True
            if self.current[1] < goal[1]: vy =  1
            else: vy =  -1
        else: # vel is x
            if self.current[0] < goal[0]: vx =  1
            else: vx =  -1
        
        self.owner.sx += vx
        self.owner.sy += vy

        if self.owner.sx % self.dim == 0 and self.owner.sy % self.dim == 0:
            self.current = self.path.pop(0)
            popped = True

        ##print ("current={}, goal={} ".format(self.current, goal), end='')
        ##print ("vel=({},{}) ".format(vx, vy), end='')
        ##print ("top={} atGoal={} ".format(str(dbgtop), str(dbgpopped)), end='')
        ##print ("Moved to ({},{})".format(self.owner.sx, self.owner.sy))

    def move2(self):
        if self.vel > 0 and self.owner.sx < self.tgtx:
            xvel, yvel = self.owner.direction.xy()
            self.owner.sx += xvel
            #self.owner.sx += self.vel
        else:
            self.vel = 0

    def move2map(self, x, y):
        self.tgtx = self.dim * x
        #self.tgty = self.dim * y
        self.vel = 1

    def __repr__(self):
        response = "dim={} current={} goal={}".format(self.dim, self.current, self.goal)
        response += '\n        goal_queue={}-{}'.format(len(self.goal_queue), str(self.goal_queue))
        response += '\n        path={}-{}'.format(len(self.path), str(self.path))
        return response 

