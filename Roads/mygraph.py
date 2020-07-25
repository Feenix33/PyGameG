'''
graph implementation from python.org/doc/essays/graphs
04 add weights
'''
import random


def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if start not in graph:
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath: return newpath
    return None

def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if start not in graph:
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest

def price_path(edge, path):
    cost = 0

    for n in range(len(path)-1):
        node = path[n] + path[n+1]
        cost += edge[node]
        #print ('{}{}=|{}|'.format('    ', 'node', node))
        #print ('{}{}=|{}|'.format('    ', 'cost', edge[node]))

    return cost


if __name__ == "__main__":
    graph = {'A': ['B', 'C'],
             'B': ['C', 'D'],
             'C': ['D'],
             'D': ['C'],
             'E': ['F'],
             'F': ['C']}
    edge = {'AB': 1, 'AC': 1, 
            'BC': 1, 'BD': 1,
            'CD': 1,
            'DC': 1,
            'EF': 1,
            'FC': 1,
            }
    #edge = {'AB': 1, 'AC': 2, 'BC': 3, 'BD': 4, 'CD': 5, 'DC': 6, 'EF': 7, 'FC': 8, }

    #path = find_path(graph, 'A', 'D')
    #print ('{}=|{}|'.format('path', path))

    all_path = find_all_paths(graph, 'A', 'D')
    short_path = []
    short_cost = 99999999
    print ('{}=|{}|'.format('all_path', all_path))
    for path in all_path:
        print ('{}=|{}|'.format('path', path), end='')
        print (' '*4, end='')
        cost = price_path(edge, path)
        print ('{}=|{}|'.format('cost', cost))
        if cost < short_cost:
            short_cost = cost
            short_path = path
        elif cost == short_cost:
            if random.randint(0, 9) < 5:
                short_cost = cost
                short_path = path

    print ('{}=|{}|'.format('short_path', short_path), end='')
    print (' '*4, end='')
    print ('{}=|{}|'.format('short_cost', short_cost))

    #short_path = find_shortest_path(graph, 'A', 'D')
    #print ('{}=|{}|'.format('short_path', short_path))
