'''
    gamemap.py
    01 - Added Flow Field
    02 - Adding distance map
    Versions are not backwards compatible


    map representation passible == 0
'''

import heapq
import collections
import random

#
# Map
#
class GameMap:
    def __init__(self, width=0, height=0, gc=None):

        self.width = width
        self.height = height
        self.tiles = [[0 for y in range(self.height)] for x in range(self.width)]
        self.flow =  None
        self.goal = (-1,-1)
        self.distxy = [[0 for y in range(self.height)] for x in range(self.width)]
        self.gc = gc # graphics component

        if self.gc: self.gc.owner = self


    def read_from_file(self, fname='map.dat'):
        with open(fname, "r") as reader:
            txt_map = reader.readlines()

        self.width = int(txt_map[0][1:])
        y = 0
        for line in txt_map:
            if line[0] != '#':
                for x in range(self.width):
                        self.tiles[x][y] = 1
                y += 1
        self.height = y

    def make_map_from(self, width, height, map_str):
        self.width = width
        self.height = height
        self.tiles = [[0 for y in range(self.height)] for x in range(self.width)]
        n = 0
        for y in range(self.height):
            for x in range(self.width):
                if map_str[n] == '.':
                    self.tiles[x][y] = 0
                elif map_str[n] == '#':
                    self.tiles[x][y] = 1
                else:
                    self.tiles[x][y] = -1
                n += 1

    #
    # Generic Routines
    #
    def make_map(self):
        self.dumb()
        pass

    def dumb(self):
        self.width = 20
        self.height = 10
        self.tiles = [[0 for y in range(self.height)] for x in range(self.width)]
        for x in range(5, 15):
            self.tiles[x][3] = 1
            self.tiles[x][8] = 1

    def dump(self,t=None, path=None):
        for y in range(self.height):
            for x in range(self.width):
                if t=='dist':
                    ch = "{:3d}".format(self.distxy[x][y])
                else:
                    if (x,y) == self.goal: ch = 'S'
                    elif self.tiles[x][y] == 0: ch = '.'
                    elif self.tiles[x][y] == 1: ch = '#'
                    else: ch = '?'
                    if path and (x,y) in path:
                        ch = "x"
                print (ch, end="")
            print()


    def set_goal(self, pt):
        self.goal = pt

    '''
    def make_distance_map_original(self):
        frontier = Queue()
        frontier.put(self.goal)
        self.distance = dict()
        self.distance[self.goal] = 0

        while not frontier.empty():
            current = frontier.get()
            for next in self.neighbors(current):
                if next not in self.distance:
                    frontier.put(next)
                    self.distance[next] = 1 + self.distance[current]
    '''

    def make_distance_map(self):
        self.distxy = [[-1 for y in range(self.height)] for x in range(self.width)]

        frontier = Queue()
        frontier.put(self.goal)
        self.distxy[self.goal[0]][self.goal[1]] = 0

        while not frontier.empty():
            current = frontier.get()
            for next in self.neighbors(current):
                if self.distxy[next[0]][next[1]] == -1:
                    frontier.put(next)
                    self.distxy[next[0]][next[1]] = 1 + self.distxy[current[0]][current[1]]

    #
    # Pretend and real setters / getters
    #

    #
    # Pathfinding Routines 
    #
    def build_a_path(self, start, maxn=1000):
        ndist, nx, ny = 10000000, -1, -1
        imat = start
        path = []
        ntimes = maxn # punch out if we can't find the goal
    
        while imat != self.goal:
            neighs = self.neighbors(imat)
            for nei in neighs:
                x, y = nei
                d = self.distxy[x][y]
                if d < ndist:
                    ndist, nx, ny = d, x, y
                if d == ndist:
                    if random.random() > 0.5:
                        ndist, nx, ny = d, x, y
            path.append((nx, ny))
            imat = (nx, ny)
            ntimes -= 1
            if ntimes < 0: break

        return path

    def cost(self, from_node, to_node):
        x, y = to_node
        return self.tiles[x][y]

    def passable(self, id):
        x,y = id
        #return self.tiles[x][y] > 0
        return self.tiles[x][y] == 0
    
    def in_bounds(self, id):
        x,y = id
        return 0 <= x < self.width and 0 <= y < self.height

    def neighbors(self, id):
        x,y = id
        results = [(x+1, y), (x,y-1), (x-1,y), (x,y+1)]
        # if (x+y) % 2 == 0: results.reverse() # aestethics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def path(self, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in self.neighbors(current):
                #print ('{}=[{}]'.format('next', next))
                new_cost = cost_so_far[current] + self.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost
                    frontier.put (next, priority)
                    came_from[next] = current

        # cme added because combining find and path creation
        if goal not in came_from:
            return []

        # Create the path
        current = goal
        path = []
        while current != start:
            #print ("Path: {} | {}".format(str(current), str(path)))
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path


    def make_flow(self, goalxy=None):
        self.flow =  [[(0,0) for y in range(self.height)] for x in range(self.width)]
        if not goalxy:
            goalxy = self._goal
        if not goalxy:
            print ("ERROR: No goal")
            return
        frontier = Queue()
        frontier.put(goalxy)
        came_from = dict()
        came_from[goalxy] = None

        #print ("frontier={} {} ".format(frontier.empty(), frontier))

        while not frontier.empty():
            current = frontier.get()
            #print ("Current = ", current)
            #print ("Neighbors = ", self.neighbors(current))
            #for next in graph.neighbors(current):
            for next in self.neighbors(current):
                #print ("next={}".format(next))
                if next not in came_from:
                    frontier.put(next)
                    came_from[next] = current

        #came_from[goalxy] = "goal"
        #print ("came_from = {}".format(came_from))
        flow = [[' ' for y in range(self.height)] for x in range(self.width)]
        #for k,v in came_from.items():
        #    x,y = k
        #    flow[x][y] = v

        x,y = goalxy
        flow[x][y] = "G"

        for y in range(self.height):
            for x in range(self.width):
                if (x,y) in came_from and came_from[(x,y)]:
                    xc, yc = came_from[(x,y)]
                    if x == xc: # vertical change
                        if y < yc:
                            self.flow[x][y] = (0,1) #"v"
                        else:
                            self.flow[x][y] = (0,-1) #"^"
                    else:
                        if x < xc:
                            self.flow[x][y] = (1, 0) #">"
                        else:
                            self.flow[x][y] = (-1, 0) #"<"


#
# Queues for Pathfinding
#
class Queue:
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, x):
        self.elements.append(x)
    
    def get(self):
        return self.elements.popleft()

class PriorityQueue:
    def __init__(self):
        self.elements = []
    def empty(self):
        return len(self.elements) == 0
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    def get(self):
        return heapq.heappop(self.elements)[1]


if __name__ == '__main__':
    print ("Self Test\n")

    #         '....5....0
    #         '0123456789
    map_str = '......###.'\
              '........#.'\
              '...###..#.'\
              '.##.....#.'\
              '..........'   # 04

    world = GameMap()
    #world.make_map()
    world.make_map_from(10, 5, map_str)
    world.set_goal((3, 1))
    world.make_distance_map()

    world.dump()
    print()

    world.dump('dist')
    print()

    path = world.build_a_path(( 7, 3))
    print()
    world.dump(path=path)

    print ("\nFini")
