'''
wang2c.py

Build image/maze with wang2c tiles
Trying to be generic
'''
import pprint
import random
from PIL import Image



def build_wang2c_database():
    '''by index is the value of each side, by dir is the matches that have the key'''
    tiledb = {} # empty database
    for j in range(16):
        n = (j%2) + 2*(j//8)
        e = j % 4
        s = (j//2) % 4
        w = ((j//4)%2)*2 + (j//8)
        tiledb[j] = {'n':n, 'w':w, 's':s, 'e':e}

    edgedb = {'n':{}, 'e':{}, 's':{}, 'w':{}}

    for key,dv in tiledb.items():
        for dex in ['n','e','s','w']:
            if dv[dex] in edgedb[dex]:
                edgedb[dex][dv[dex]].append(key)
            else:
                edgedb[dex][dv[dex]] = [key]

    tiledb[None] = {'n':None, 'w':None, 's':None, 'e':None}
    for dex in ['n','e','s','w']:
        edgedb[dex][None] = None

    return tiledb, edgedb

def random_fill(width, height, tiledb, edgedb):
    def lu(x,y): # helper function for lookups
        if 0 <= x < width and 0 <= y < height: return array[x][y]
        return None

    #array = [[-1 for y in range(height)] for x in range(width)]
    array = [[None for y in range(height)] for x in range(width)]

    # build initial set
    #for y in range(height):
    #    for x in range(width):
    #        if (x+y)%2: array[x][y] = (x+y) % 15 #random.randint(0,15)

    if 0: print (array_str(array, width, height))

    for y in range(height):
        for x in range(width):
            #if lu(x, y) == -1:
            if lu(x, y) == None:
                if 0: print (x, y)
                #tiles = candidates( lu(x-1, y), lu(x, y+1), lu(x+1, y), lu(x, y-1), tiledb, tile2db, ndb, wdb, sdb, edb)
                tiles = tile_candidates( lu(x, y-1), lu(x+1, y), lu(x, y+1), lu(x-1, y), tiledb, edgedb)
                array[x][y] = random.choice(tiles)
                if 0: print ("From ", tiles, "selected ", array[x][y])
                if 0: print (array_str(array, width, height))

    return array

def tile_candidates(tn, tw, ts, te, tiledb, edgedb):
    # get all the candidates 
    # use the opposite side of what tile is referenced
    n_candidates = edgedb['n'][tiledb[tn]['s']]
    w_candidates = edgedb['e'][tiledb[tw]['w']]
    s_candidates = edgedb['s'][tiledb[ts]['n']]
    e_candidates = edgedb['w'][tiledb[te]['e']]

    if 0: print (" "*4, tn, tw, ts, te)
    if 0: print (" "*8, 'N', n_candidates, tiledb[tn]['n'], tn)
    if 0: print (" "*8, 'W', w_candidates, tiledb[tw]['w'], tw)
    if 0: print (" "*8, 'S', s_candidates, tiledb[ts]['s'], ts)
    if 0: print (" "*8, 'E', e_candidates, tiledb[te]['e'], te)

    # build a list of candidates, use a list in case there is a None entry
    candidates = []
    if n_candidates: candidates.append(set(n_candidates))
    if w_candidates: candidates.append(set(w_candidates))
    if s_candidates: candidates.append(set(s_candidates))
    if e_candidates: candidates.append(set(e_candidates))

    if not candidates:
        if 0: print ("ALL")
        return list(tiledb.keys())[:-1]

    #get the intersection of all the candidates
    rtn = list(set.intersection(*candidates))
    return rtn


def array_str(array, width, height):
    rtn = ""
    for y in range(height):
        for x in range(width):
            if array[x][y] is not None:
                rtn += "{:3d}".format(array[x][y])
            else:
                rtn += "  ."
        rtn += "\n"
    rtn += "\n"
    rtn += "\n"
    return rtn

def extract_wang2c_tiles(fname):
    inImg = Image.open(fname)
    #build boxes
    box = [*range(16)]
    box[ 4] = ( 0*32,  0*32,  1*32,  1*32)  # 00
    box[ 3] = ( 1*32,  0*32,  2*32,  1*32)  # 06 // 01
    box[14] = ( 2*32,  0*32,  3*32,  1*32)  # 14 // 02
    box[ 6] = ( 3*32,  0*32,  4*32,  1*32)  # 12 // 03

    box[10] = ( 0*32,  1*32,  1*32,  2*32)  # 05 // 04
    box[ 7] = ( 1*32,  1*32,  2*32,  2*32)  # 07 // 05
    box[15] = ( 2*32,  1*32,  3*32,  2*32)  # 15 // 06
    box[13] = ( 3*32,  1*32,  4*32,  2*32)  # 13 // 07

    box[ 1] = ( 0*32,  2*32,  1*32,  3*32)  # 01 // 08
    box[ 9] = ( 1*32,  2*32,  2*32,  3*32)  # 03 // 09
    box[11] = ( 2*32,  2*32,  3*32,  3*32)  # 11 // 10
    box[12] = ( 3*32,  2*32,  4*32,  3*32)  # 09 // 11

    box[ 0] = ( 0*32,  3*32,  1*32,  4*32)  # 00 // 12
    box[ 2] = ( 1*32,  3*32,  2*32,  4*32)  # 02 // 13
    box[ 5] = ( 2*32,  3*32,  3*32,  4*32)  # 10 // 14
    box[ 8] = ( 3*32,  3*32,  4*32,  4*32)  # 08 // 15

    region = []
    for b in box: region.append(inImg.crop(b))

    return region

#==============================================================================
    
if __name__ == '__main__':


    width = 25
    height = 25


    pp = pprint.PrettyPrinter(width=61, compact=True)
    # build the database for wang2c
    tiledb, edgedb = build_wang2c_database()
    if False:
        pp.pprint (tiledb)
        print ()
        pp.pprint (edgedb)

    # test the database lookups
    if False:
        print ("Keys")
        keys = list(tiledb.keys())[:-1]
        print (keys)

    # build the image/maze
    imarray = random_fill(width, height, tiledb, edgedb) 
    #print (array_str(imarray, width, height))

    # load the tileset
    tilenames = ['beam', 'border', 'brench', 'cliff', 'glob', 'ground', 'island',
            'path', 'pcb', 'roof', 'sandgrass', 'seasand', 'square', 'steps',
            'lido', 'patch', 'terrain', 'wang2c']
    fpath = "c:/Dev/assets/Wang2c/"
    filename = random.choice(tilenames)
    #filename = 'wang2c'
    region = extract_wang2c_tiles(fpath+filename+".png")

    # save the image using the tileset
    outImg = Image.new('RGB', (height*32, width*32), 0)

    for y in range(height):
        for x in range(width):
            box = (x*32, y*32, (x+1)*32, (y+1)*32)
            n = imarray[x][y]
            outImg.paste(region[n], box)

    outImg.save("tiles.png")
