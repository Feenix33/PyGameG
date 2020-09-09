"""
wang2e.py

possibilities:
    see if we can delete tiledb and just keep tile2db
    pass in options
    wrap xy image
    make a path and then fill in the rest
    simplify databases
    
    extend to next set
"""
import random
from PIL import Image


def create2edge():
    # the creation is not generic and heavily depends on the wang2e 4x4 layout 
    # and the patterns accompanying that layout
    # These four database are what tileNos map to a 0 or 1 edge
    ndb = {0:[], 1:[]} 
    wdb = {0:[], 1:[]}
    sdb = {0:[], 1:[]}
    edb = {0:[], 1:[]}
    #tiledb is given a tile number, what is the edge on each side, a 1 or 0?
    tiledb = {}

    # tile2db is given an tile number, what is the edge on each side, a 1 or 0?
    tile2db = {}
    # build the nwse set by counting to 16
    for n in range(16):
        ndb[n%2].append(n)
        wdb[(n//2)%2].append(n)
        sdb[(n//4)%2].append(n)
        edb[(n//8)%2].append(n)
        tiledb[n] = [n%2, (n//2)%2, (n//4)%2, (n//8)%2]
        tile2db[n] = {'n':n%2, 'w':(n//2)%2, 's':(n//4)%2, 'e':(n//8)%2}
    # add 'None' entries
    ndb[None] = None
    wdb[None] = None
    sdb[None] = None
    edb[None] = None
    tiledb[None] = [None, None, None, None]
    tile2db[None] = {'n':None, 'w':None, 's':None, 'e':None}
    return tiledb, tile2db, ndb, wdb, sdb, edb

def candidates(tn, tw, ts, te, tiledb, tile2db, ndb, wdb, sdb, edb):
    # get all the candidates 
    # use the opposite side of what tile is referenced
    n_candidates = ndb[tile2db[tn]['s']]
    w_candidates = wdb[tile2db[tw]['e']]
    s_candidates = sdb[tile2db[ts]['n']]
    e_candidates = edb[tile2db[te]['w']]

    # build a list of candidates, use a list in case there is a None entry
    candidates = []
    if n_candidates: candidates.append(set(n_candidates))
    if w_candidates: candidates.append(set(w_candidates))
    if s_candidates: candidates.append(set(s_candidates))
    if e_candidates: candidates.append(set(e_candidates))

    #get the intersection of all the candidates
    rtn = list(set.intersection(*candidates))
    return rtn


def build_array(tiledb, tile2db, ndb, wdb, sdb, edb, nr=10, nc=20):
    def lu(x,y): # helper function for lookups
        if 0 <= x < nr and 0 <= y < nc: return array[x][y]
        return None

    array = [[-1 for y in range(nc)] for x in range(nr)]

    # build initial set
    for x in range(nr):
        for y in range(nc):
            if (x+y)%2: array[x][y] = random.randint(0,15)

    # fill in the holes
    for x in range(nr):
        for y in range(nc):
            if lu(x, y) == -1:
                tiles = candidates( lu(x-1, y), lu(x, y+1), lu(x+1, y), lu(x, y-1),
                            tiledb, tile2db, ndb, wdb, sdb, edb)
                array[x][y] = random.choice(tiles)

    return array


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


if __name__ == '__main__':

    nrow = 15
    ncol = 20

    tilenames = ["angular", "border", "celtic", "glob", "laser", "path",
            "pully", "quad", "square", "tilt", "urban", "walkway", "wang2e"]
    fpath = "c:/Dev/assets/Wang/"
    filename = random.choice(tilenames)
    region = extract_tiles(fpath+filename+".png")

    #Build the array
    tiledb, tile2db, ndb, wdb, sdb, edb = create2edge()
    iray = build_array(tiledb, tile2db, ndb, wdb, sdb, edb, nrow, ncol)

    '''
    for x in range(nrow):
        for y in range(ncol):
            print ("{:3d}".format(iray[x][y]), end="")
        print ()
    print ()
    '''
    outImg = Image.new('RGB', (ncol*32, nrow*32), 0)

    for x in range(nrow):
        for y in range(ncol):
            box = (y*32, x*32, (y+1)*32, (x+1)*32)
            n = iray[x][y]
            outImg.paste(region[n], box)

    outImg.save("tiles.png")
