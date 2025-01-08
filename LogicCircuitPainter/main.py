from LogicCircuiteer import *

parser = ExprParser()

print("Format used in entering expressions (AND = &, OR = |, NOT = ~), have a nice trial!")
parser.in_expr = input("Enter the expression: ")

while True:
    try:
        parser.parse()
        print(f"Parsed expression: {parser.expr}\n")
        break
    except Exception:
        parser.in_expr = input("Invalid Expression! Enter expression: ")

painter = Painter(parser.postfix_expr)
painter.draw_exp()

image_name = input("Enter name of output image (with extension, if not entered defaults to .jpg): ")
while True:
    try:
        painter.save(image_name)
        break
    except Exception:
        image_name = input("Invalid Name! Enter name of output image (with extension, if not entered defaults to .jpg): ")