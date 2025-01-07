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
1. ![a &amp; b &#124; &#126;c](LogicCircuitPainter/examples/example_1.jpg)
2. ![c &#124; (&#126;b &amp; a) &#124; (&#126;d &amp; b)](LogicCircuitPainter/examples/example_2.jpg)
3. ![a &#124; &#126;(b &amp; &#126;(a &amp; d)) &#124; (b &amp; &#126;(b &#124; (d &amp; &#126;c)))](LogicCircuitPainter/examples/example_3.jpg)
```

