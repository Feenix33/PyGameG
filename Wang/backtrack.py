'''
sidewinder.py
Build a maze using the sidewinder algorithm
binary counts are n=1 e=2 s=4 w=8
'''
import random
from PIL import Image

#directions = ['n', 's', 'e', 'w']
#DX = {'n':0, 's':0, 'e':1, 'w':-1}
#DY = {'n':-1, 's':1, 'e':0, 'w':0}
#OPP = {'n':'s': 's':'n', 'e':'w', 'w':'e'}
directions = [1, 4, 2, 8]
DX = {1:0, 4:0, 2:1, 8:-1}
DY = {1:-1, 4:1, 2:0, 8:0}
OPP = {1:4, 4:1, 2:8, 8:2}

def carve_passages_from(cx, cy, grid, width, height):
    global directions, DX, DY, OPP
    #import pdb; pdb.set_trace()

    dirs = directions
    random.shuffle(dirs)
    #print_maze(grid, nrow, ncol)
    for d in dirs:
        nx, ny = cx + DX[d], cy+DY[d]

        if 0 <= ny < height and 0 <= nx < width and grid[nx][ny] == 0:
            grid[cx][cy] += d
            grid[nx][ny] += OPP[d]
            carve_passages_from(nx, ny, grid, width, height)

def backtrack(nrow, ncol):
    global directions, DX, DY, OPP

    maze = [[0 for y in range(ncol)] for x in range(nrow)]

    carve_passages_from(0, 0, maze, ncol, nrow)


    return maze


def extract_tiles(fname):
    inImg = Image.open(fname)
    #build boxes
    box = []
    box.append(( 0*32,  3*32,  1*32,  4*32))  # 00 // 12
    box.append(( 0*32,  2*32,  1*32,  3*32))  # 01 // 08
    box.append(( 1*32,  3*32,  2*32,  4*32))  # 02 // 13
    box.append(( 1*32,  2*32,  2*32,  3*32))  # 03 // 09

    box.append(( 0*32,  0*32,  1*32,  1*32))  # 04 // 00
    box.append(( 0*32,  1*32,  1*32,  2*32))  # 05 // 04
    box.append(( 1*32,  0*32,  2*32,  1*32))  # 06 // 01
    box.append(( 1*32,  1*32,  2*32,  2*32))  # 07 // 05

    box.append(( 3*32,  3*32,  4*32,  4*32))  # 08 // 15
    box.append(( 3*32,  2*32,  4*32,  3*32))  # 09 // 11
    box.append(( 2*32,  3*32,  3*32,  4*32))  # 10 // 14
    box.append(( 2*32,  2*32,  3*32,  3*32))  # 11 // 10

    box.append(( 3*32,  0*32,  4*32,  1*32))  # 12 // 03
    box.append(( 3*32,  1*32,  4*32,  2*32))  # 13 // 07
    box.append(( 2*32,  0*32,  3*32,  1*32))  # 14 // 02
    box.append(( 2*32,  1*32,  3*32,  2*32))  # 15 // 06

    region = []
    for b in box: region.append(inImg.crop(b))

    return region

def build_image(maze, nrow, ncol, outname='grid'):
    tilenames = ["angular", "border", "celtic", "glob", "laser", "path",
            "pully", "quad", "square", "tilt", "urban", "walkway", "wang2e"]
    fpath = "c:/Dev/assets/Wang/"
    filename = random.choice(tilenames)
    filename = "wang2e"
    region = extract_tiles(fpath+filename+".png")

    outImg = Image.new('RGB', (ncol*32, nrow*32), 0)

    for y in range(nrow):
        for x in range(ncol):
            box = (x*32, y*32, (x+1)*32, (y+1)*32)
            n = maze[x][y]
            outImg.paste(region[n], box)

    outfile = outname + '.png'
    outImg.save(outfile)


def print_maze(maze, nrow, ncol):
    for y in range(nrow):
        for x in range(ncol):
            if maze[x][y]:
                print ("{:3d}".format(maze[x][y]), end="")
            else:
                print (" . ", end="")
        print ()
    print ()
    print ()
    
if __name__ == '__main__':

    nrow = 20
    ncol = 20

    maze = backtrack(nrow, ncol)

    print_maze(maze, nrow, ncol)
    build_image(maze, nrow, ncol, 'backtrack')
