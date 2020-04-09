"""
    trains.py
    Trains following a path between cities

"""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import random
import pygame as pg
import math


CAPTION = "Trains 02"
SCREEN_SIZE = (400, 400)
MAX_FPS = 30

from pygame.locals import ( RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT,)


class City(pg.sprite.Sprite):
    _radius = 10 # City radius
    def __init__(self, x, y, n, cityclr="red", textclr="white"):
        super(City, self).__init__()
        self.image = pg.Surface((2*City._radius, 2*City._radius))
        self.image.fill( pg.Color("magenta") )
        font = pg.font.SysFont(pg.font.get_default_font(), 2*City._radius)
        text = font.render(str(n), True, pg.Color(textclr))
        pg.draw.circle(self.image, pg.Color(cityclr), (City._radius, City._radius), City._radius)
        self.image.blit(text, 
                ((2*City._radius - text.get_width()) //2, (2*City._radius - text.get_height()) //2))
        self.image.set_colorkey(pg.Color("magenta"), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.n = n

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def x(self): return self.rect.centerx
    def y(self): return self.rect.centery
    def name(self): return self.n
    def center(self): return self.rect.center


class Link(pg.sprite.Sprite):
    _width = 3
    _marker = 0.9
    _log = 0
    def __init__(self, n, nodes, cnm_base="black", cnm_marker="red"):
        super(Link, self).__init__()
        self.n = n
        self.clr_base = pg.Color(cnm_base)
        self.clr_marker = pg.Color(cnm_marker)
        self.orig = nodes[(n // 100)-1]
        self.dest = nodes[(n % 100)-1]
        self.dist = pg.Vector2(self.orig.center()).distance_to(
                pg.Vector2(self.dest.center()))
        dx = self.dest.x()-self.orig.x() 
        dy = self.dest.y()-self.orig.y()
        self._marker = pg.Vector2(self.orig.x()+Link._marker*dx, self.orig.y()+Link._marker*dy)
        self.angle = math.atan2(dy, dx)
        #if dx == 0: self.angle += math.pi
        self.angle %= 2*math.pi
        if Link._log:
            print ("Link {} from {} to {} distance {:.1f} at angle {:.1f}".format(
                n, self.orig.name(), self.dest.name(), self.dist, math.degrees(self.angle)))

    def marker(self):
        return (int(self._marker.x),int(self._marker.y))

    def draw(self, surf):
        pg.draw.line(surf, self.clr_base, self.orig.center(), self.dest.center(), Link._width)
        pg.draw.line(surf, self.clr_marker, self.marker(), self.dest.center(), Link._width*2)
        #pg.draw.line(surf, self.clr_marker, (int(self.marker.x),int(self.marker.y)), self.dest.center(), Link._width*2)

    def name(self): return self.n
    #def angle(self): return self.angle

    def norig(self): return self.orig.name()
    def ndest(self): return self.dest.name()


def find_link(links, name):
    for link in links:
        if name == link.name(): return link
    return None

def find_links_from(links, n):
    matches = []
    for link in links:
        if link.norig() == n:
            matches.append(link)
    return matches
            

class Train(pg.sprite.Sprite):
    _width = 11
    _height = 7
    _head = 3
    _log = 0
    def __init__(self, n, orig, vel=2, cnm_body="blue", cnm_head="yellow"):
        super(Train, self).__init__()
        self.n = n
        self.link = None
        self.velocity = vel
        self.vel = pg.Vector2(1, 0)
        self.traveled = 0
        #self.pos = pg.Vector2(self.orig.x(), self.orig.y())
        self.pos = pg.Vector2(0, 0)
        self.rotation = 0
        self.clrbody = pg.Color(cnm_body)
        self.clrhead = pg.Color(cnm_head)
        self.prepare_sprite()
        self._in_city = orig
        self.at_dest = True


    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def update(self):
        if self.link == None: return
        self.traveled += self.velocity
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        if self.traveled >= self.link.dist:
            self.rect.centerx = self.link.dest.x()
            self.rect.centery = self.link.dest.y()
            self.at_dest = True
            self._in_city = self.link.dest
            self.link = None
            #print ("Train {} is at {}".format(self.n, self._in_city.name()))
        self.rect.center = (int(round(self.pos.x)), int(round(self.pos.y)))

    def set_link(self, link):
        self.link = link
        self.traveled = 0
        self.pos.x = self.link.orig.x()
        self.pos.y = self.link.orig.y()
        self.vel.x = self.velocity * math.cos(self.link.angle)
        self.vel.y = self.velocity * math.sin(self.link.angle)

        self.at_dest = False
        self.in_city = None
        self.rotation = math.degrees(self.link.angle)
        self.prepare_sprite()

        if Train._log:
            print ("Train {} on link {} from orig {} to dest {} at vel of {} = ({:.2f},{:.2f})".format(
                    self.n, self.link.n, self.link.orig.n, self.link.dest.n,
                    self.velocity, self.vel.x, self.vel.y))

    def prepare_sprite(self):
        #redraw the train then rotate it 
        self.image = pg.Surface((Train._width, Train._height))
        self.image.fill( pg.Color("magenta") )
        self.image.set_colorkey(pg.Color("magenta"), RLEACCEL)
        self.image.fill(self.clrbody)
        self.rect = self.image.get_rect()
        pg.draw.rect(self.image, self.clrhead, (self.rect.right-Train._head, self.rect.top, Train._head, self.rect.height))
        pg.draw.line(self.image, self.clrhead, (self.rect.right, self.rect.top), (self.rect.right, self.rect.bottom), 5)

        self.image = pg.transform.rotate(self.image, -self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def name(self): return self.n
    def at_destination(self): return self.at_dest
    def in_city(self): return self._in_city.name()
    def city_in(self): return self._in_city.name()


def new_routes(trains, links):
    for train in trains:
        if train.at_destination():
            #print("Processing train {} at {}".format(train.name(), train.city_in()))
            paths = find_links_from(links, train.city_in())
            train.set_link(random.choice(paths))

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)

    screen = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()
    running = True

    cities = [] 
    cities.append( City(100, 100, 1, "yellow", "black") )
    cities.append( City(300, 100, 2, "yellow", "black") )
    cities.append( City(100, 300, 3, "lightgray", "black") )
    cities.append( City(300, 300, 4, "lightgray", "black") )
    cities.append( City(200,  50, 5, "lightgray", "white") )

    links = []
    links.append( Link(102, cities) )
    links.append( Link(201, cities) )
    links.append( Link(103, cities) )
    links.append( Link(301, cities) )
    links.append( Link(203, cities) )
    links.append( Link(302, cities) )
    links.append( Link(204, cities) )
    links.append( Link(304, cities) )
    links.append( Link(401, cities) )
    links.append( Link(501, cities) )
    links.append( Link(504, cities) )
    links.append( Link(205, cities) )

    trains = []
    trains.append( Train(1, random.choice(cities)) )
    trains.append( Train(2, random.choice(cities), 3, cnm_body="green"))
    trains.append( Train(3, random.choice(cities), 1, "darkorange"))

    #specific_link = find_link(links, 102)
    #if specific_link == None: print ("No link")
    #else: trains[0].set_link( specific_link )

    while running:
        for event in pg.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            elif event.type == QUIT:
                running = False

        screen.fill(pg.Color("skyblue"))

        # update elements
        for train in trains:
            train.update()

        new_routes(trains, links)

        # Draw screen elements
        for link in links: link.draw(screen)
        for city in cities: city.draw(screen)
        for train in trains: train.draw(screen)


        #pg.display.update()
        pg.display.flip()

        clock.tick_busy_loop(MAX_FPS)

    pg.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()
