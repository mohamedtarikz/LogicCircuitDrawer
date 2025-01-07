import math

import sympy as sp

import schemdraw
from schemdraw import elements as elm
from schemdraw import Drawing
from schemdraw import logic

from enum import Enum

schemdraw.use('matplotlib') # to export image as .jpg not .svg

print("Format used in entering expressions (AND = &, OR = |, NOT = ~), have a nice trial!")

in_expr = input("Enter the expression: ")

while True:
    try:
        expr = sp.parse_expr(in_expr)  # '&' for AND, '|' for OR, '~' for NOT
        break
    except SyntaxError:
        in_expr = input(f"Error: '{in_expr}' is not in valid format, Enter the expression: ")

print("Parsed Expression:", expr)

def postfix(expression):
    '''
    recursive function to convert the expression to a postfix expression

    :return: list of postfix expression
    '''

    if expression.is_Atom:
        return [str(expression)]
    elif isinstance(expression, sp.Not):
        return postfix(expression.args[0]) + ["~"]
    elif isinstance(expression, sp.Or):
        return  sum((postfix(arg) for arg in expression.args), []) + ["|"] * (len(expression.args) - 1)
    elif isinstance(expression, sp.And):
        return sum((postfix(arg) for arg in expression.args), []) + ["&"] * (len(expression.args) - 1)

post = postfix(expr)

# function to move drawing brush to a certain coordinate
def move_to(drawing, target_pos, current_pos = None, diff_x=0.0, diff_y=0.0):
    '''
    moves drawing brush to a specific coordinate

    :param drawing: drawing canvas
    :param target_pos: target coordinate
    :param current_pos: current coordinate
    :param diff_x: constant to be added to the x-coordinate of the target
    :param diff_y: constant to be added to the y-coordinate of the target
    '''

    if current_pos is None:
        current_pos = drawing.here
    dx = target_pos[0] - current_pos[0] + diff_x
    dy = target_pos[1] - current_pos[1] + diff_y
    drawing.move(dx, dy)

def magnitude(start, end):
    '''
    calculates the length between two points

    :return: length between start and end
    '''

    x = (end[0] - start[0]) ** 2
    y = (end[1] - start[1]) ** 2
    return math.sqrt(x + y)

def from_path(drawing, start, end, ratio: float=1.0, diff_x=0.0, diff_y=0.0):
    '''
    moves drawing brush to a position on the line between two points (by ratio)

    :param drawing: drawing canvas
    :param ratio: how much of the line is before the brush
    :param diff_x: constant to be added to the x-coordinate of the target
    :param diff_y: constant to be added to the y-coordinate of the target
    '''

    if ratio > 1 or ratio < 0 or start is None or end is None:
        raise ValueError("ratio must be between 0 and 1")
    x_pos = (end[0] - start[0]) * ratio
    y_pos = (end[1] - start[1]) * ratio
    move_to(drawing, (start[0] + x_pos, start[1] + y_pos), diff_x=diff_x, diff_y=diff_y)

def at_path(drawing, start, end, len=1.0, diff_x=0.0, diff_y=0.0):
    '''
    moves drawing brush to a position on the line between two points (by length)

    :param drawing: drawing canvas
    :param len: length of the part of the line before the brush
    :param diff_x: constant to be added to the x-coordinate of the target
    :param diff_y: constant to be added to the y-coordinate of the target
    '''

    length = magnitude(start, end)
    ratio = len / length
    from_path(drawing, start, end, ratio, diff_x, diff_y)


class Gate(Enum):
    '''
    Enumeration of GATES used in the circuit drawing
    '''

    Not = 1
    Or = 2
    And = 3

class Node:
    def __init__(self, position, diff_x=0, diff_y=0):
        self.pos = (position[0]+diff_x, position[1]+diff_y)

nodes = []

def draw_line(drawing, start, end):
    '''
    draws a line from start to end
    '''

    move_to(drawing, start)
    drawing += elm.Line().to(end)

def connect_nodes(drawing, node1: Node=None, node2: Node=None, gate: Gate=None):
    '''
    connects two nodes with a gate (possibly one node if the gate is a NOT)

    :param drawing: drawing canvas
    :param gate: specified gate to use
    '''

    if node1 is None and node2 is None:
        raise Exception("You must specify node1 or node2")
    if gate == Gate.Not:
        if node1 is None and node2 is None:
            raise Exception("You must specify node1 or node2")
        if node1 is None:
            move_to(drawing, node2.pos, diff_x=0.5)
            not_gate = logic.Not().right()
            drawing += not_gate
            nodes.append(Node(not_gate.absanchors['out'], diff_x=1))
            draw_line(drawing, node2.pos, not_gate.absanchors['in1'])
        elif node2 is None:
            move_to(drawing, node1.pos, diff_x=0.5)
            not_gate = logic.Not().right()
            drawing += not_gate
            nodes.append(Node(not_gate.absanchors['out'], diff_x=1))
            draw_line(drawing, node1.pos, not_gate.absanchors['in1'])
    else:
        move_to(drawing, (max(node2.pos[0],node1.pos[0]) + 0.5, (node2.pos[1] + node1.pos[1]) / 2))
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

def draw_exp():
    '''
    Main drawing function that draws the circuit

    :param expr_tree: the expression tree to draw
    '''
    global height
    global d
    global post
    for node in post:
        if node == '~':
            a = nodes[-1]
            nodes.pop()
            connect_nodes(d, node1=a, gate=Gate.Not)
        elif node == '&':
            a = nodes[-1]
            b = nodes[-2]
            nodes.pop()
            nodes.pop()
            connect_nodes(d, node1=a, node2=b, gate=Gate.And)
        elif node == '|':
            a = nodes[-1]
            b = nodes[-2]
            nodes.pop()
            nodes.pop()
            connect_nodes(d, node1=a, node2=b, gate=Gate.Or)
        else:
            move_to(d, (0, height))
            dot = elm.Dot(open=True).label(node, loc='left')
            d += dot
            nodes.append(Node(dot.absanchors['center']))
            height += 1

draw_exp()

image_name = input("Enter your image name (with extension, if not entered default is .png): ")

while True:
    if image_name.__contains__('.'):
        try:
            d.save(image_name)
            break
        except Exception:
            image_name = input("Invalid input! Enter your image name (with extension, if not specified default is .jpg): ")
    else:
        try:
            image_name += ".jpg"
            d.save(image_name)
            break
        except Exception:
            image_name = input("Invalid input! Enter your image name (with extension, if not specifieded default is .jpg): ")