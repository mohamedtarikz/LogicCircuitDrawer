# LogicCircuitDrawer
Takes a logical expression from user and draws a logic circuit in an image

## Dependencies:
```
1- sympy
2- schemdraw & matplotlib
```
The syntax/format for input (AND = &, OR = |, NOT = ~), those are the only gates used currently.

## Examples:
```
1- ![a & b | ~c][LogicCircuitPainter/examples/example_1.jpg]
2- ![c | (~b & a) | (~d & b)][LogicCircuitPainter/examples/example_2.jpg]
3- ![a | ~(b & ~(a & d)) | (b & ~(b | (d & ~c)))][LogicCircuitPainter/examples/example_3.jpg]
```
