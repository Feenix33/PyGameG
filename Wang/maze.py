'''
maze.py
Base routines to draw a maze on a grid
'''
import random
from PIL import Image

def build_maze(nrow, ncol, start, end):
    def hline(x1,x2,y):
        if x1>x2: x1,x2 = x2,x1
        for x in range(x1, x2):
            array[x][y] = '|'
            if x==x1: array[x][y] = '+'
            if x==x2: array[x][y] = '+'

    def vline(x,y1,y2):
        if y1>y2: y1,y2 = y2,y1
        for y in range(y1, y2):
            array[x][y] = '-'
            if y == y1: array[x][y] = '+'
            if y == y2: array[x][y] = '+'

    array = [[None for y in range(ncol)] for x in range(nrow)]

    points = []
    points.append((random.randint(0,nrow), random.randint(0,ncol)))
    points.append(end)
    pt1 = start
    for pt2 in points:
        hline(pt1[0], pt2[0], pt1[1])
        vline(pt2[0], pt2[1], pt1[1])
        pt1 = pt2
        print_maze(array, nrow, ncol)

    return array


def print_maze(array, nrow, ncol):
    for x in range(nrow):
        for y in range(ncol):
            if array[x][y]:
                #print ("{:1d}".format(array[x][y]), end="")
                print (array[x][y], end="")
            else:
                print (".", end="")
        print ()
    print ()
    print ()
    
if __name__ == '__main__':

    nrow = 8 #15
    ncol = 10 #20

    array = build_maze(nrow, ncol, (5, 7), (1, 1))

    print_maze(array, nrow, ncol)
