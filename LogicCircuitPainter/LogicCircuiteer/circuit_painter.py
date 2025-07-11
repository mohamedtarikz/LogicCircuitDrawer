import schemdraw
from schemdraw import elements as elm
from schemdraw import Drawing
from schemdraw import logic
from enum import Enum

schemdraw.use('matplotlib')  # to export image as .jpg not .svg


class Gate(Enum):
    '''
    Enumeration of GATES used in the circuit drawing
    '''

    Not = logic.Not
    Or = logic.Or
    And = logic.And
    Nand = logic.Nand
    Nor = logic.Nor
    Xor = logic.Xor
    Xnor = logic.Xnor


class Node:
    def __init__(self, position, diff_x=0.0, diff_y=0.0):
        self.pos = (position[0] + diff_x, position[1] + diff_y)


class Painter:
    def __init__(self, expression):
        self.expression = expression
        self.drawing = Drawing()
        self.height = 0
        self.nodes = []

    def move_to(self, target_pos, current_pos=None, diff_x=0.0, diff_y=0.0):
        '''
        moves drawing brush to a specific coordinate

        :param target_pos: target coordinate
        :param current_pos: current coordinate
        :param diff_x: constant to be added to the x-coordinate of the target
        :param diff_y: constant to be added to the y-coordinate of the target
        '''

        if current_pos is None:
            current_pos = self.drawing.here
        dx = target_pos[0] - current_pos[0] + diff_x
        dy = target_pos[1] - current_pos[1] + diff_y
        self.drawing.move(dx, dy)

    def draw_line(self, start, end):
        '''
        draws a line from start to end
        '''

        self.move_to(start)
        self.drawing += elm.Line().to(end)

    def connect_nodes(self, node1: Node = None, node2: Node = None, gate: Gate = None):
        '''
        connects two nodes with a gate (possibly one node if the gate is a NOT)

        :param gate: specified gate to use
        '''

        if node1 is None and node2 is None:
            raise Exception("You must specify node1 or node2")
        if gate == Gate.Not:
            if node1 is None and node2 is None:
                raise Exception("You must specify node1 or node2")
            if node1 is None:
                self.move_to(node2.pos)
                not_gate = gate.value().right()
                self.drawing += not_gate
                self.nodes.append(Node(not_gate.absanchors['out'], diff_x=1.1))
                self.draw_line(node2.pos, not_gate.absanchors['in1'])
            elif node2 is None:
                self.move_to(node1.pos)
                not_gate = gate.value().right()
                self.drawing += not_gate
                self.nodes.append(Node(not_gate.absanchors['out'], diff_x=1.1))
                self.draw_line(node1.pos, not_gate.absanchors['in1'])
        else:
            self.move_to((max(node2.pos[0], node1.pos[0]) + 0.5, (node2.pos[1] + node1.pos[1]) / 2))

            try:
                in_gate = gate.value().right()
            except Exception as e:
                raise Exception("Unexpected Gate!")

            self.drawing += in_gate
            self.nodes.append(Node(in_gate.absanchors['out']))
            if node1.pos[1] > node2.pos[1]:
                self.draw_line(node1.pos, in_gate.absanchors['in1'])
                self.draw_line(node2.pos, in_gate.absanchors['in2'])
            else:
                self.draw_line(node1.pos, in_gate.absanchors['in2'])
                self.draw_line(node2.pos, in_gate.absanchors['in1'])

    def draw_circuit(self):
        '''
        Main drawing function that draws the circuit
        '''
        print(f"postfix: {self.expression}")
        i = 0
        while i < len(self.expression):
            if self.expression[i] == '~':
                a = self.nodes[-1]
                self.nodes.pop()
                self.connect_nodes(node1=a, gate=Gate.Not)
            elif self.expression[i] == '&' or self.expression[i] == '|' or self.expression[i] == '^':
                a = self.nodes[-1]
                b = self.nodes[-2]
                self.nodes.pop()
                self.nodes.pop()
                if i != (len(self.expression) - 1) and self.expression[i + 1] == '~':
                    if self.expression[i] == '&':
                        self.connect_nodes(node1=a, node2=b, gate=Gate.Nand)
                    elif self.expression[i] == '|':
                        self.connect_nodes(node1=a, node2=b, gate=Gate.Nor)
                    else:
                        self.connect_nodes(node1=a, node2=b, gate=Gate.Xnor)
                    i += 1
                else:
                    if self.expression[i] == '&':
                        self.connect_nodes(node1=a, node2=b, gate=Gate.And)
                    elif self.expression[i] == '|':
                        self.connect_nodes(node1=a, node2=b, gate=Gate.Or)
                    else:
                        self.connect_nodes(node1=a, node2=b, gate=Gate.Xor)
            else:
                self.move_to((0, self.height))
                dot = elm.Dot(open=True).label(self.expression[i], loc='left')
                self.drawing += dot
                self.nodes.append(Node(dot.absanchors['center']))
                self.height += 1
            i += 1

    def save(self, filename):
        if '.' in filename:
            try:
                self.drawing.save(filename)
            except Exception:
                print(f"exception: {Exception}")
                raise Exception
        else:
            try:
                filename += ".jpg"
                self.drawing.save(filename)
            except Exception:
                print(f"exception: {Exception}")
                raise Exception
