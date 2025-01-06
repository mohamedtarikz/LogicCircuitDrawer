import sympy as sp

in_expr = input("Enter the expression: ")

expr = sp.parse_expr(in_expr)  # '&' for AND, '|' for OR, '~' for NOT
print("Parsed Expression:", expr)

def parse_tree(expression):
    if expression.is_Atom:  # Input node (e.g., A, B, C)
        return {"type": "INPUT", "value": str(expression)}
    elif isinstance(expression, sp.Not):  # NOT gate
        return {"type": "NOT", "inputs": [parse_tree(expression.args[0])]}
    elif isinstance(expression, sp.And):  # AND gate
        return {"type": "AND", "inputs": [parse_tree(arg) for arg in expression.args]}
    elif isinstance(expression, sp.Or):  # OR gate
        return {"type": "OR", "inputs": [parse_tree(arg) for arg in expression.args]}
    else:
        raise ValueError(f"Unsupported expression: {expression}")

# Generate the tree
tree = parse_tree(expr)

import math

# %matplotlib inline
import schemdraw
from schemdraw import elements as elm
from schemdraw import Drawing
from schemdraw import logic

schemdraw.use('matplotlib')

def move_to(drawing, target_pos, current_pos = None, diff_x=0, diff_y=0):
    if current_pos is None:
        current_pos = drawing.here
    dx = target_pos[0] - current_pos[0] + diff_x
    dy = target_pos[1] - current_pos[1] + diff_y
    drawing.move(dx, dy)

def magnitude(start, end):
    x = (end[0] - start[0]) ** 2
    y = (end[1] - start[1]) ** 2
    return math.sqrt(x + y)

def from_path(drawing, start, end, ratio: float=1.0, diff_x=0, diff_y=0):
    if ratio > 1 or ratio < 0 or start is None or end is None:
        raise ValueError("ratio must be between 0 and 1")
    x_pos = (end[0] - start[0]) * ratio
    y_pos = (end[1] - start[1]) * ratio
    move_to(drawing, (start[0] + x_pos, start[1] + y_pos), diff_x=diff_x, diff_y=diff_y)

def at_path(drawing, start, end, len=1.0, diff_x=0, diff_y=0):
    length = magnitude(start, end)
    ratio = len / length
    from_path(drawing, start, end, ratio, diff_x, diff_y)

from enum import Enum

class Gate(Enum):
    Not = 1
    Or = 2
    And = 3

class Node:
    def __init__(self, position, diff_x=0, diff_y=0):
        self.pos = (position[0]+diff_x, position[1]+diff_y)

nodes = []

def draw_line(drawing, start, end):
    move_to(drawing, start)
    drawing += elm.Line().to(end)

def connect_nodes(drawing, node1: Node=None, node2: Node=None, gate: Gate=None):
    if node1 is None and node2 is None:
        raise Exception("You must specify node1 or node2")
    if gate == Gate.Not:
        if node1 is None and node2 is None:
            raise Exception("You must specify node1 or node2")
        if node1 is None:
            move_to(drawing, node2.pos, diff_x=1)
            not_gate = logic.Not().right()
            drawing += not_gate
            nodes.append(Node(not_gate.absanchors['out'], diff_x=1))
            draw_line(drawing, node2.pos, not_gate.absanchors['in1'])
        elif node2 is None:
            move_to(drawing, node1.pos, diff_x=1)
            not_gate = logic.Not().right()
            drawing += not_gate
            nodes.append(Node(not_gate.absanchors['out'], diff_x=1))
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

d = Drawing()
height = 0

def draw_exp(expr_tree):
    global height
    global d
    if len(str(expr_tree)) == 1:
        move_to(d, (0, height))
        dot = elm.Dot(open=True).label(str(expr_tree), loc='left')
        d += dot
        nodes.append(Node(dot.absanchors['center']))
        height += 1
    elif isinstance(expr_tree, sp.Not):
        draw_exp(expr_tree.args[0])
        a = nodes[-1]
        nodes.pop()
        connect_nodes(d, node1=a, gate=Gate.Not)
    elif isinstance(expr_tree, sp.And):
        draw_exp(expr_tree.args[0])
        draw_exp(expr_tree.args[1])
        a = nodes[-1]
        b = nodes[-2]
        nodes.pop()
        nodes.pop()
        connect_nodes(d, node1=a, node2=b, gate=Gate.And)
    elif isinstance(expr_tree, sp.Or):
        draw_exp(expr_tree.args[0])
        draw_exp(expr_tree.args[1])
        a = nodes[-1]
        b = nodes[-2]
        nodes.pop()
        nodes.pop()
        connect_nodes(d, node1=a, node2=b, gate=Gate.Or)


draw_exp(expr)

d.save('real_draw.jpg')