import math

# %matplotlib inline
import schemdraw
from schemdraw import elements as elm
from schemdraw import Drawing
from schemdraw import logic
import matplotlib
import warnings

# Suppress warnings about non-interactive backend
warnings.filterwarnings("ignore", category=UserWarning, module="schemdraw.backends.mpl")

# Set the backend to Agg
matplotlib.use('Agg')

# Use the matplotlib backend
schemdraw.use('matplotlib')

def move_to(drawing, target_pos, current_pos=None, diff_x=0, diff_y=0):
    if current_pos is None:
        current_pos = drawing.here
    dx = target_pos[0] - current_pos[0] + diff_x
    dy = target_pos[1] - current_pos[1] + diff_y
    drawing.move(dx, dy)

def magnitude(start, end):
    x = (end[0] - start[0]) ** 2
    y = (end[1] - start[1]) ** 2
    return math.sqrt(x + y)

def at_line(drawing, start, end, ratio: float=1.0, diff_x=0, diff_y=0):
    if ratio > 1 or ratio < 0 or start is None or end is None:
        raise ValueError("ratio must be between 0 and 1")
    x_pos = (end[0] - start[0]) * ratio
    y_pos = (end[1] - start[1]) * ratio
    move_to(drawing, (start[0] + x_pos, start[1] + y_pos), diff_x=diff_x, diff_y=diff_y)

def goto(drawing, start, end, len=1.0, diff_x=0, diff_y=0):
    length = magnitude(start, end)
    ratio = len / length
    at_line(drawing, start, end, ratio, diff_x, diff_y)

from enum import Enum

class Gate(Enum):
    Not = 1
    Or = 2
    And = 3

class Node:
    def __init__(self, position):
        self.pos = position

nodes = []

def draw_line(drawing, start, end):
    move_to(drawing, start)
    drawing += elm.Line().to(end)

def connect_nodes(drawing, node1: Node, node2: Node, gate: Gate):
    if node1 is None and node2 is None:
        raise Exception("You must specify node1 or node2")
    if gate == Gate.Not:
        if node1 is None and node2 is None:
            raise Exception("You must specify node1 or node2")
        if node1 is None:
            move_to(drawing, node2.pos, diff_x=1)
            not_gate = logic.Not().right()
            drawing += not_gate
            nodes.append(Node(not_gate.absanchors['out']))
            draw_line(drawing, node2.pos, not_gate.absanchors['in1'])
        elif node2 is None:
            move_to(drawing, node1.pos, diff_x=1)
            not_gate = logic.Not().right()
            drawing += not_gate
            nodes.append(Node(not_gate.absanchors['out']))
            draw_line(drawing, node1.pos, not_gate.absanchors['in1'])
    else:
        move_to(drawing, (max(node2.pos[0],node1.pos[0]) + 1, (node2.pos[1] + node1.pos[1]) / 2))
        if gate == Gate.And:
            in_gate = logic.And().right()
        elif gate == Gate.Or:
            in_gate = logic.Or().right()
        else:
            raise Exception("Unexpected Gate!")
        drawing += in_gate
        nodes.append(Node(in_gate.absanchors['out']))
        if node1.pos[1] > node2.pos[1]:
            draw_line(drawing, node1.pos, in_gate.absanchors['in1'])
            draw_line(drawing, node2.pos, in_gate.absanchors['in2'])
        else:
            draw_line(drawing, node1.pos, in_gate.absanchors['in2'])
            draw_line(drawing, node2.pos, in_gate.absanchors['in1'])


def main_draw(_vars):
    with Drawing() as d:
        n = len(_vars)
        for i in range(n):
            init_dot = elm.Dot(open=True).label(_vars[i], loc='top')
            d += init_dot
            elm.Line().down().length(n)
            dot = elm.Dot()
            d += dot
            nodes.append(Node(dot.absanchors['center']))
            move_to(d, init_dot.absanchors['center'], diff_x=1)
            n -= 1
        while len(nodes):
            a = nodes[-1]
            nodes.pop()
            if len(nodes):
                b = nodes[-1]
                nodes.pop()
                connect_nodes(d, a, b, Gate.And)
        d.save('my_draw.jpg')

inputs = []

n = int(input('Enter number of vars: '))

for _ in range(n):
    inputs.append(input('Enter variable: '))

main_draw(inputs)