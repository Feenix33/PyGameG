'''
gamemap.py
'''

import heapq

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

class GameMap:
    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.tiles = [[0 for y in range(self.height)] for x in range(self.width)]
        self.stations = []
        self.trucks = []


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
                        if line[x] == 's': self.stations.append((x, y))
                        if line[x] == 't': self.trucks.append((x, y))
                y += 1
        self.height = y

    def make_map(self):
        #self.roadrect(4, 10, 30, 10)
        #self.hroad(( 4, 10), 20)
        #self.vroad(( 4, 10), 10)
        #self.hroad(( 4, 20), 25)
        #self.vroad((14, 20),  2)
        self.make_map_from_file()


    def get_trucks_coords(self):
        return self.trucks

    def get_stations_coords(self):
        return self.stations

    def hroad(self, start, length, value=1):
        x,y = start
        for _ in range(length):
            self.tiles[x][y] = value
            x += 1

    def vroad(self, start, length, value=1):
        x,y = start
        for _ in range(length):
            self.tiles[x][y] = value
            y += 1

    def roadrect(self, xs, ys, xw, yh): 
        for x in range(xs, xs+xw):
            self.tiles[x][ys] = True
            self.tiles[x][ys+yh-1] = True
        for y in range(ys, ys+yh):
            self.tiles[xs][y] = True
            self.tiles[xs+xw-1][y] = True

    def cost(self, from_node, to_node):
        x, y = to_node
        return self.tiles[x][y]

    def passable(self, id):
        x,y = id
        return self.tiles[x][y] > 0
    
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


    def dump(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.tiles[x][y] == 0:
                    print (" ", end="")
                else:
                    print (self.tiles[x][y], end="")
            print ("|")
