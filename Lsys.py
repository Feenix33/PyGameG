import turtle

#SYSTEM_RULES = {}  # generator system rules for l-system

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
    def dump(self):
        print ("Axiom = ", self.axiom)
        print ("Rules")
        for key,value in self.rules.items():
            print ("    k= ", key, "  value= ", value)

    def derivation(self, steps):
        full = self.derivation_full(steps)
        return full[-1]

    def derivation_full(self, steps):
        derived = [self.axiom]  # seed
        for _ in range(steps):
            next_seq = derived[-1]
            next_axiom = [self.rule(char) for char in next_seq]
            derived.append(''.join(next_axiom))
        return derived

    def rule(self, sequence):
        if sequence in self.rules:
            return self.rules[sequence]
        return sequence

def lsys_test():
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

    system = plant
    iterations = 4
    #alpha_zero = 0
    render_string = system.derivation(iterations)

    # Set turtle parameters and draw L-System
    r_turtle = set_turtle(system.alpha_zero)  # create turtle object
    turtle_screen = turtle.Screen()  # create graphics window
    turtle_screen.screensize(1500, 1500)
    draw_l_system(r_turtle, render_string, system.segment_length, system.angle)  # draw model
    turtle_screen.exitonclick()


def main():
    #raw_test()
    lsys_test()




if __name__ == "__main__":
    main()
