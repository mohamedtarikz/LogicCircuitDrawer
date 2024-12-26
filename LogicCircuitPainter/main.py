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

def draw_main():
    with Drawing() as d:
        a = elm.Dot(open=True).label('A', loc='top')
        a_line = elm.Line().down().length(5)
        move_to(d, a.absanchors['center'], diff_x=1)
        b = elm.Dot(open=True).label('B', loc='top')
        b_line = elm.Line().down().length(5)

        at_line(d, b_line.start, b_line.end, ratio=0.2)
        elm.Dot()
        elm.Line().right().length(1)

        goto(d, a_line.start, a_line.end, len=1.5)
        elm.Dot()
        elm.Line().right().length(2)

        logic.And().right().anchor('in2')

        elm.Line().right().length(2).label('OUT', loc='bottom')

        # Save the figure to a file
        d.save('my_draw.jpg')

draw_main()