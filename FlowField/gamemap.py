'''
gamemap.py
'''

import heapq
import collections

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

    world_width = 50
    world_height = 30

#
# Map
#
class GameMap:
    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.tiles = [[0 for y in range(self.height)] for x in range(self.width)]
        #self.flow =  [[(0,0) for y in range(self.height)] for x in range(self.width)]
        self.flow =  None
        self._goal = None
        self._sources = []



    def make_map_from_file(self):
        with open("plan.txt", "r") as reader:
            txt_map = reader.readlines()

        self.width = int(txt_map[0][1:])
        y = 0
        for line in txt_map:
            if line[0] != '#':
                for x in range(self.width):
                    if line[x] in ['r', 's', 't']:
                        self.tiles[x][y] = 1
                y += 1
        self.height = y

    def dumb_map(self):
        #self.make_map_from_file()
        h2 = self.height //2
        h4 = self.height //4
        w2 = self.width //2
        w4 = self.width //4
        for x in range(w4, w4+w2):
            self.tiles[x][h4] = 1
            self.tiles[x][h2] = 1
            self.tiles[x][h4+h2] = 1
        self._goal = ( 1, 1)
        self._sources.append((18, 5))
        self._sources.append(( 8, 8))

    #
    # Generic Routines
    #
    def make_map(self):
        self.dumb_map()
        self.make_flow(goalxy=self._goal)
        pass

    def dump(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.tiles[x][y] == 0: ch = "."
                else: ch = self.tiles[x][y]

                if self._goal and (x,y) == self._goal: ch = "G"
                if (x,y) in self._sources: ch = "S"
                print (ch, end='')
            print ("|")

        if not self.flow: return

        print ("\nFlow Field")
        for y in range(self.height):
            for x in range(self.width):
                mov = self.flow[x][y]
                if mov == (0,1): ch = "v"
                elif mov == (0, -1): ch = "^"
                elif mov == (1, 0): ch = ">"
                elif mov == (-1, 0): ch = "<"
                else: mov = " "
                if (x,y) == self._goal: ch = "G"
                if (x,y) in self._sources: ch = "S"
                print (ch, end='')
            print()


        for y in range(self.height):
            for x in range(self.width):
                print ("{:2d}".format(self.flow[x][y][0]), end="")

            print ("        ", end='')
            for x in range(self.width):
                print ("{:2d}".format(self.flow[x][y][1]), end="")

            print ()


    #
    # Pretend and real setters / getters
    #
    def set_tile(self, x, y, value):
        if self.in_bounds((x,y)):
            self.tiles[x][y] = value % 16   ## magic number
    def increment_tile(self, x, y):
        if self.in_bounds((x,y)):
            self.tiles[x][y] = (self.tiles[x][y]+1) % 16   ## magic number
    def toggle_tile(self, x, y):
        if self.in_bounds((x,y)):
            self.tiles[x][y] = (self.tiles[x][y]+1) % 2

    @property
    def goal(self):
        return self._goal
    @goal.setter
    def goal(self, val):
        self._goal = val # TODO add check if valid

    @property
    def sources(self):
        return self._sources
    def add_source(self, val):
        self._sources.append(val)

    #
    # Pathfinding Routines 
    #

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


