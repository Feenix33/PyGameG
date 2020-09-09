'''
sidewinder.py
Build a maze using the sidewinder algorithm
binary counts are n=1 e=2 s=4 w=8
'''
import random
from PIL import Image

def sidewinder_maze(nrow, ncol):
    maze = [[0 for y in range(ncol)] for x in range(nrow)]
    for y in range(nrow):
        run_start = 0
        for x in range(ncol):
            if y>0 and (x+1 == ncol or random.randint(0,1)):
                #print ("N ", end="")
                # end run and carve north
                cell = run_start + random.randint(0, x-run_start)
                maze[cell][y] += 1
                maze[cell][y-1] += 4
                run_start = x+1
                #print (' |', end="")
                #for xx in range(ncol): print (maze[xx][y], end='')
                #print ('| ', end="")
            elif x+1 < ncol:
                #print ("E ", end="")
                # carve east
                maze[x][y] += 2
                maze[x+1][y] += 8
            #print (x, y, run_start, maze[x][y])
        #print_maze(maze, nrow, ncol)
        
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
    for b in box:
        region.append(inImg.crop(b))


    return region

def build_image(maze, nrow, ncol):
    tilenames = ["angular", "border", "celtic", "glob", "laser", "path",
            "pully", "quad", "square", "tilt", "urban", "walkway", "wang2e"]
    fpath = "c:/Dev/assets/Wang/"
    filename = random.choice(tilenames)
    #filename = "wang2e"
    region = extract_tiles(fpath+filename+".png")

    outImg = Image.new('RGB', (ncol*32, nrow*32), 0)

    for y in range(nrow):
        for x in range(ncol):
            box = (x*32, y*32, (x+1)*32, (y+1)*32)
            n = maze[x][y]
            outImg.paste(region[n], box)

    outImg.save("sidewinder.png")


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

    maze = sidewinder_maze(nrow, ncol)

    print_maze(maze, nrow, ncol)
    build_image(maze, nrow, ncol)
