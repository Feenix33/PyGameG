from PIL import Image

def oldstuff():
    region = inImg.crop(box01)
    for y in range(0, 128, 32):
        for x in range(0, 128, 32):
            new_box = (x, y, x+32, y+32)
            outImg.paste(region[n], new_box)
            n += 1

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

if __name__ == "__main__":

    nrow = 4
    ncol = 4
    iray = [[10 for y in range(ncol)] for x in range(nrow)]

    #region = extract_tiles("wang2e.png")
    fname = "c:/Dev/assets/Wang/angular.png"
    fname = "c:/Dev/assets/Wang/border.png"
    fname = "c:/Dev/assets/Wang/celtic.png"
    fname = "c:/Dev/assets/Wang/glob.png"
    fname = "c:/Dev/assets/Wang/path.png"
    fname = "c:/Dev/assets/Wang/pully.png"
    fname = "c:/Dev/assets/Wang/quad.png"
    fname = "c:/Dev/assets/Wang/square.png"
    fname = "c:/Dev/assets/Wang/tilt.png"
    fname = "c:/Dev/assets/Wang/walkway.png"
    fname = "c:/Dev/assets/Wang/wang2e.png"
    fname = "c:/Dev/assets/Wang/laser.png"
    fname = "c:/Dev/assets/Wang/urban.png"
    region = extract_tiles(fname)

    outImg = Image.new('RGB', (nrow*32, ncol*32), 0)

    for y in range(ncol):
        for x in range(nrow):
            box = (x*32, y*32, (x+1)*32, (y+1)*32)
            n = iray[x][y]
            outImg.paste(region[n], box)

    outImg.save("tiles.png")

