"""
create.py
Create the basic 2-edge tileset
"""
import random


def create2edge(tiledb, tile2db, ndb, wdb, sdb, edb):
    # build the nwse set by counting to 16
    for n in range(16):
        ndb[n%2].append(n)
        wdb[(n//2)%2].append(n)
        sdb[(n//4)%2].append(n)
        edb[(n//8)%2].append(n)
        tiledb[n] = [n%2, (n//2)%2, (n//4)%2, (n//8)%2]
        tile2db[n] = {'n':n%2, 'w':(n//2)%2, 's':(n//4)%2, 'e':(n//8)%2}
    ndb[None] = None
    wdb[None] = None
    sdb[None] = None
    edb[None] = None
    tiledb[None] = [None, None, None, None]
    tile2db[None] = {'n':None, 'w':None, 's':None, 'e':None}

def candidates(tn, tw, ts, te, tiledb, tile2db, ndb, wdb, sdb, edb):
    n_candidates = ndb[tile2db[tn]['s']]
    w_candidates = wdb[tile2db[tw]['e']]
    s_candidates = sdb[tile2db[ts]['n']]
    e_candidates = edb[tile2db[te]['w']]
    #print("n cand: ", tile2db[tn]['s'],n_candidates)
    #print("w cand: ",tile2db[tw]['e'],w_candidates)
    #print("s cand: ",tile2db[ts]['n'],s_candidates)
    #print("e cand: ",tile2db[te]['w'],e_candidates)

    candidates = []
    if n_candidates: candidates.append(set(n_candidates))
    if w_candidates: candidates.append(set(w_candidates))
    if s_candidates: candidates.append(set(s_candidates))
    if e_candidates: candidates.append(set(e_candidates))
    #print (candidates)

    #get the intersection of all the candidates
    rtn = list(set.intersection(*candidates))
    return rtn


def test_show_create(tiledb, tile2db, ndb, wdb, sdb, edb):
    print ('North DB', ndb)
    print ('West  DB', wdb)
    print ('South DB', sdb)
    print ('East  DB', edb)
    print ('Tile  DB', tiledb)
    print ('Tile2 DB', tile2db)
    print (tile2db[2]['n'],tile2db[2]['w'],tile2db[2]['s'],tile2db[2]['e'])

def test_check_individual(tiledb, tile2db, ndb, wdb, sdb, edb):
    print ( 4, candidates(None,  6,  5, None, tiledb, tile2db, ndb, wdb, sdb, edb))
    print ( 6, candidates(None, 14,  7,  4, tiledb, tile2db, ndb, wdb, sdb, edb))
    print (14, candidates(None, 12, 15,  6, tiledb, tile2db, ndb, wdb, sdb, edb))
    print (12, candidates(None, None, 13, 14, tiledb, tile2db, ndb, wdb, sdb, edb))

    print ( 5, candidates( 4,  7,  1, None, tiledb, tile2db, ndb, wdb, sdb, edb))
    print ( 7, candidates( 6, 15,  3,  5, tiledb, tile2db, ndb, wdb, sdb, edb))
    print (15, candidates(14, 13, 11,  7, tiledb, tile2db, ndb, wdb, sdb, edb))
    print (13, candidates(12, None,  9, 15, tiledb, tile2db, ndb, wdb, sdb, edb))

    print ( 1, candidates( 5,  3,  0, None, tiledb, tile2db, ndb, wdb, sdb, edb))
    print ( 3, candidates( 7, 11,  2,  1, tiledb, tile2db, ndb, wdb, sdb, edb))
    print (11, candidates(15,  9, 10,  3, tiledb, tile2db, ndb, wdb, sdb, edb))
    print ( 9, candidates(13, None,  8, 11, tiledb, tile2db, ndb, wdb, sdb, edb))

    print ( 0, candidates( 1,  2, None, None, tiledb, tile2db, ndb, wdb, sdb, edb))
    print ( 2, candidates( 3, 10, None,  0, tiledb, tile2db, ndb, wdb, sdb, edb))
    print (10, candidates(11,  8, None,  2, tiledb, tile2db, ndb, wdb, sdb, edb))
    print ( 8, candidates( 9, None, None, 10, tiledb, tile2db, ndb, wdb, sdb, edb))



def test_build_array(tiledb, tile2db, ndb, wdb, sdb, edb, nr=10, nc=20):
    def lu(x,y):
        if 0 <= x < nr and 0 <= y < nc: return array[x][y]
        return None
    def lu_dbg(x,y):
        if 0 <= x < nr and 0 <= y < nc:
            print ("array[{},{}]={}".format(x,y, array[x][y]))
            return array[x][y]
        print ("array[{},{}]=N/A".format(x,y))
        return None
    def dump():
        for x in range(nr):
            for y in range(nc):
                print ("{:3d}".format(array[x][y]), end="")
            print ()
        print ()

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

    dump()


if __name__ == '__main__':
    ndb = {0:[], 1:[]}
    wdb = {0:[], 1:[]}
    sdb = {0:[], 1:[]}
    edb = {0:[], 1:[]}
    tiledb = {}
    tile2db = {}

    create2edge(tiledb, tile2db, ndb, wdb, sdb, edb)
    #test_show_create(tiledb, tile2db, ndb, wdb, sdb, edb)
    #test_check_individual(tiledb, tile2db, ndb, wdb, sdb, edb)
    test_build_array(tiledb, tile2db, ndb, wdb, sdb, edb, 10, 15)


    print ("Fini")
