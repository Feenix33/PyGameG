"""
Lsys.py
Generate an L-system and draw it with turtle or pygame

"""
#for pygame version
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import math
import pygame as pg
from pygame.locals import ( K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT,)

#for turtle version
import turtle


#SYSTEM_RULES = {}  # generator system rules for l-system

def pg_test(lsys):
    CAPTION = "L-System"
    SCREEN_SIZE = (1200, 750)
    MAX_FPS = 30

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)

    screen = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()
    running = True

    screen.fill(pg.Color("white"))

    # draw the L-System
    my_turtle = pgTurtle(screen, SCREEN_SIZE[0]//4, SCREEN_SIZE[1]*2//3)
    my_turtle.width(3)
    draw_l_system(my_turtle, lsys.render_string(),lsys.segment_length, math.radians(lsys.angle))  # draw model 


    pg.display.update()
    pg.display.flip()

    while running:
        for event in pg.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            elif event.type == QUIT:
                running = False
        clock.tick_busy_loop(MAX_FPS)
    pg.quit()
    sys.exit()

class pgTurtle:
    def __init__(self, surf, x, y):
        self.surf = surf
        self.pen = True #true if pen is down
        self.penclr = pg.Color("black")
        self._heading = 0
        self.x = x
        self.y = y
        self._width = 1

    def forward(self, segment):
        start = [int(self.x), int(self.y)]
        self.x += segment * math.cos(self._heading)
        self.y += segment * math.sin(self._heading)
        end = [int(self.x), int(self.y)]
        if self.pen:
            pg.draw.line(self.surf, self.penclr, start, end, self._width)
    def pu(self):
        self.pen = False # false = pen up
    def pd(self):
        self.pen = True # true = pen down
    def right(self, angle):
        self._heading += angle
    def left(self, angle):
        self._heading -= angle
    def position(self):
        return (self.x, self.y)
    def goto(self, position):
        self.x = position[0]
        self.y = position[1]
    def heading(self):
        return self._heading
    def setheading(self, angle):
        self._heading = angle
    def width(self, w):
        self._width = w


#def pg_draw(turtle, lstring, segment, angle):
#    stack = []

def draw_l_system(turtle, SYSTEM_RULES, seg_length, angle):
    stack = []
    for command in SYSTEM_RULES:
        turtle.pd()
        if command in ["F", "G", "R", "L"]:
            turtle.forward(seg_length)
        elif command == "f":
            turtle.pu()  # pen up - not drawing
            turtle.forward(seg_length)
        elif command == "+":
            turtle.right(angle)
        elif command == "-":
            turtle.left(angle)
        elif command == "[":
            stack.append((turtle.position(), turtle.heading()))
        elif command == "]":
            turtle.pu()  # pen up - not drawing
            position, heading = stack.pop()
            turtle.goto(position)
            turtle.setheading(heading)


def set_turtle(alpha_zero):
    r_turtle = turtle.Turtle()  # recursive turtle
    r_turtle.screen.title("L-System Derivation")
    r_turtle.speed(0)  # adjust as needed (0 = fastest)
    r_turtle.setheading(alpha_zero)  # initial heading
    return r_turtle


class LSystem:
    def __init__(self, axiom, rules, angle=90, alpha_zero=0, segment_length=10):
        self.axiom = axiom
        self.rules = rules
        self.angle = angle
        self.alpha_zero = alpha_zero
        self.segment_length = segment_length
        self.derived = []
    def dump(self):
        print ("Axiom = ", self.axiom)
        print ("Rules")
        for key,value in self.rules.items():
            print ("    k= ", key, "  value= ", value)

    def derivation(self, steps):
        full = self.derivation_full(steps)
        return full[-1]

    def derivation_full(self, steps):
        self.derived = [self.axiom]  # seed
        for _ in range(steps):
            next_seq = self.derived[-1]
            next_axiom = [self.rule(char) for char in next_seq]
            self.derived.append(''.join(next_axiom))
        return self.derived

    def rule(self, sequence):
        if sequence in self.rules:
            return self.rules[sequence]
        return sequence
    def render_string(self):
        #print (self.derived[-1])
        return self.derived[-1]


def generate_lsys():
    dragon = LSystem(
            axiom='L',
            rules={ 'L':'L+R+', 'R':'-L-R'},
            angle=90,
            )

    koch_curve = LSystem(
            axiom='F',
            rules={ 'F':'F-F+F+F-F' } ,
            angle=90,
            )

    sierpinski = LSystem(
            axiom='F-G-G',
            rules={ 'F':'F-G+F+G-F', 'G':'GG' },
            angle=120,
            segment_length = 20,
            )

    arrowhead = LSystem(
            axiom='F',
            rules={ 'F':'G-F-G', 'G':'F+G+F' },
            angle=-60,
            segment_length = 20,
            )

    plant = LSystem(
            axiom='G',
            rules={ 'F':'FF', 'G':'F+[[G]-G]-F[-FG]+G' },
            angle= 25,
            segment_length = 10,
            alpha_zero=90,
            )

    system = koch_curve
    iterations = 4
    #alpha_zero = 0
    render_string = system.derivation(iterations)
    return system

def lsys_test(lsys):
    # Set turtle parameters and draw L-System
    r_turtle = set_turtle(lsys.alpha_zero)  # create turtle object
    turtle_screen = turtle.Screen()  # create graphics window
    turtle_screen.screensize(1500, 1500)
    draw_l_system(r_turtle, lsys.render_string(), lsys.segment_length, lsys.angle)  # draw model
    turtle_screen.exitonclick()


def main():
    lsys = generate_lsys()
    #raw_test()
    #lsys_test(lsys)
    pg_test(lsys)



if __name__ == "__main__":
    main()
=======
"""
Lsys.py
Generate an L-system and draw it with turtle or pygame

"""
#for pygame version
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import math
import pygame as pg
from pygame.locals import ( K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT,)

#for turtle version
import turtle


#SYSTEM_RULES = {}  # generator system rules for l-system

def pg_test(lsys):
    CAPTION = "L-System"
    SCREEN_SIZE = (1200, 750)
    MAX_FPS = 30

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)

    screen = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()
    running = True

    screen.fill(pg.Color("white"))

    # draw the L-System
    my_turtle = pgTurtle(screen, SCREEN_SIZE[0]//4, SCREEN_SIZE[1]*2//3)
    my_turtle.width(3)
    draw_l_system(my_turtle, lsys.render_string(),lsys.segment_length, math.radians(lsys.angle))  # draw model 


    pg.display.update()
    pg.display.flip()

    while running:
        for event in pg.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            elif event.type == QUIT:
                running = False
        clock.tick_busy_loop(MAX_FPS)
    pg.quit()
    sys.exit()

class pgTurtle:
    def __init__(self, surf, x, y):
        self.surf = surf
        self.pen = True #true if pen is down
        self.penclr = pg.Color("black")
        self._heading = 0
        self.x = x
        self.y = y
        self._width = 1

    def forward(self, segment):
        start = [int(self.x), int(self.y)]
        self.x += segment * math.cos(self._heading)
        self.y += segment * math.sin(self._heading)
        end = [int(self.x), int(self.y)]
        if self.pen:
            pg.draw.line(self.surf, self.penclr, start, end, self._width)
    def pu(self):
        self.pen = False # false = pen up
    def pd(self):
        self.pen = True # true = pen down
    def right(self, angle):
        self._heading += angle
    def left(self, angle):
        self._heading -= angle
    def position(self):
        return (self.x, self.y)
    def goto(self, position):
        self.x = position[0]
        self.y = position[1]
    def heading(self):
        return self._heading
    def setheading(self, angle):
        self._heading = angle
    def width(self, w):
        self._width = w


#def pg_draw(turtle, lstring, segment, angle):
#    stack = []

def draw_l_system(turtle, SYSTEM_RULES, seg_length, angle):
    stack = []
    for command in SYSTEM_RULES:
        turtle.pd()
        if command in ["F", "G", "R", "L"]:
            turtle.forward(seg_length)
        elif command == "f":
            turtle.pu()  # pen up - not drawing
            turtle.forward(seg_length)
        elif command == "+":
            turtle.right(angle)
        elif command == "-":
            turtle.left(angle)
        elif command == "[":
            stack.append((turtle.position(), turtle.heading()))
        elif command == "]":
            turtle.pu()  # pen up - not drawing
            position, heading = stack.pop()
            turtle.goto(position)
            turtle.setheading(heading)


def set_turtle(alpha_zero):
    r_turtle = turtle.Turtle()  # recursive turtle
    r_turtle.screen.title("L-System Derivation")
    r_turtle.speed(0)  # adjust as needed (0 = fastest)
    r_turtle.setheading(alpha_zero)  # initial heading
    return r_turtle


class LSystem:
    def __init__(self, axiom, rules, angle=90, alpha_zero=0, segment_length=10):
        self.axiom = axiom
        self.rules = rules
        self.angle = angle
        self.alpha_zero = alpha_zero
        self.segment_length = segment_length
        self.derived = []
    def dump(self):
        print ("Axiom = ", self.axiom)
        print ("Rules")
        for key,value in self.rules.items():
            print ("    k= ", key, "  value= ", value)

    def derivation(self, steps):
        full = self.derivation_full(steps)
        return full[-1]

    def derivation_full(self, steps):
        self.derived = [self.axiom]  # seed
        for _ in range(steps):
            next_seq = self.derived[-1]
            next_axiom = [self.rule(char) for char in next_seq]
            self.derived.append(''.join(next_axiom))
        return self.derived

    def rule(self, sequence):
        if sequence in self.rules:
            return self.rules[sequence]
        return sequence
    def render_string(self):
        #print (self.derived[-1])
        return self.derived[-1]


def generate_lsys():
    dragon = LSystem(
            axiom='L',
            rules={ 'L':'L+R+', 'R':'-L-R'},
            angle=90,
            )

    koch_curve = LSystem(
            axiom='F',
            rules={ 'F':'F-F+F+F-F' } ,
            angle=90,
            )

    sierpinski = LSystem(
            axiom='F-G-G',
            rules={ 'F':'F-G+F+G-F', 'G':'GG' },
            angle=120,
            segment_length = 20,
            )

    arrowhead = LSystem(
            axiom='F',
            rules={ 'F':'G-F-G', 'G':'F+G+F' },
            angle=-60,
            segment_length = 20,
            )

    plant = LSystem(
            axiom='G',
            rules={ 'F':'FF', 'G':'F+[[G]-G]-F[-FG]+G' },
            angle= 25,
            segment_length = 10,
            alpha_zero=90,
            )

    system = koch_curve
    iterations = 4
    #alpha_zero = 0
    render_string = system.derivation(iterations)
    return system

def lsys_test(lsys):
    # Set turtle parameters and draw L-System
    r_turtle = set_turtle(lsys.alpha_zero)  # create turtle object
    turtle_screen = turtle.Screen()  # create graphics window
    turtle_screen.screensize(1500, 1500)
    draw_l_system(r_turtle, lsys.render_string(), lsys.segment_length, lsys.angle)  # draw model
    turtle_screen.exitonclick()


def main():
    lsys = generate_lsys()
    #raw_test()
    #lsys_test(lsys)
    pg_test(lsys)



if __name__ == "__main__":
    main()
