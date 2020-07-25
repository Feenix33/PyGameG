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


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[0 for y in range(self.height)] for x in range(self.width)]


    def draw(self, start=None, fini=None):
        # Summary
        rtnstr = "width={} height={}\n\n".format(self.width, self.height)

        # x/col indexes
        rtnstr += " "*4
        for x in range(self.width):
            rtnstr += "{:1d}".format(x//10)
        rtnstr += "\n"
        rtnstr += " "*4
        for x in range(self.width):
            rtnstr += "{:1d}".format(x%10)
        rtnstr += "\n"

        # map and y/row indexes
        for y in range(self.height):
            rtnstr += "{:02d}  ".format(y)
            for x in range(self.width):
                if (x,y) == start: rtnstr += str('S')
                elif (x,y) == fini: rtnstr += str('E')
                else:
                    rtnstr += str(self.tiles[x][y]) if self.tiles[x][y] > 0 else "."
            rtnstr += "\n"
        return rtnstr

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

        # Create the path
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path

def dijkstra_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        #print ('{}=[{}]'.format('current', current))

        if current == goal:
            #print ('Found the end')
            break

        for next in graph.neighbors(current):
            #print ('{}=[{}]'.format('next', next))
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put (next, priority)
                came_from[next] = current

    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def draw_tile(graph, id, style, width):
    r = "."
    if 'number' in style and id in style['number']: r = "%d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = ">"
        if x2 == x1 - 1: r = "<"
        if y2 == y1 + 1: r = "v"
        if y2 == y1 - 1: r = "^"
    if 'start' in style and id == style['start']: r = "A"
    if 'goal' in style and id == style['goal']: r = "Z"
    if 'path' in style and id in style['path']: r = "@"
    if graph.tiles[id[0]][id[1]] <= 0: r = "#" * width
    return r

def draw_grid(graph, width=2, **style):
    for y in range(graph.height):
        for x in range(graph.width):
            print("%%-%ds" % width % draw_tile(graph, (x, y), style, width), end="")
        print()

if __name__ == "__main__":
    world = GameMap(20, 10)

    world.hroad((3,1), 10)
    world.hroad((3,5), 12)
    world.vroad((3,1), 5)
    world.vroad((8,1), 8)

    start = (3,1)
    fini  = (8,2)
    fini  = (8,6)
    fini  = (3,1)
    start = (8,6)

    came, cost = dijkstra_search(world, start, fini)
    path = reconstruct_path(came, start, fini)

    '''
    print (world.draw(start=start, fini=fini))
    print ('{}=[{}]'.format('came', came))
    print ('{}=[{}]'.format('cost', cost))
    print ('{}=[{}]'.format('start', start))
    print ('{}=[{}]'.format('fini', fini))
    print ('{}=[{}]'.format('path', path))
    print ()
    '''
    print ('{}=[{}]'.format('path', path))
    print ()
    path = world.path(start, fini)
    print ('{}=[{}]'.format('path', path))

    #draw_grid(world, width=1, path=reconstruct_path(came, start, fini))
    draw_grid(world, width=1, path=path)
