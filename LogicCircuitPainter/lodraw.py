import argparse
from LogicCircuiteer import *


def main():
    parser = argparse.ArgumentParser(description='Generate logic circuit drawing from a logic expression.')
    parser.add_argument('expression', type=str, help='Logic Expression (e.g., "A & B")')
    parser.add_argument('-o', '--output', type=str,
                        help="Output file name, default extension is .jpg (optional)", default="circuit.jpg")

    args = parser.parse_args()

    try:
        expr_parser = ExprParser(args.expression)
        expr_parser.parse()
        print(f"Parsed expression: {expr_parser.expr}\n")

        painter = Painter(expr_parser.postfix_expr)
        painter.draw_circuit()

        painter.save(args.output)
    except Exception as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    main()
