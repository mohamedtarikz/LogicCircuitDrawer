# LogicCircuitDrawer
Takes a logical expression from user and draws a logic circuit in an image

## Dependencies:
```
1- sympy==1.13.3
2- schemdraw==0.19
3- matplotlib==3.10.0
```
**To install the required dependencies:**<br>
download the ```requirements.txt``` file, then run the following command
```
pip install -r requirements.txt
```
## Examples:
**The syntax/format for input (AND = &, OR = |, NOT = ~), those are the only gates used currently.**<br>
1. ![a & b | ~c](LogicCircuitPainter/examples/example_1.jpg)<br>
Logical Expression: 'a & b | ~c'<br><br>
2. ![c | (~b & a) | (~d & b)](LogicCircuitPainter/examples/example_2.jpg)<br>
Logical Expression: 'c | (~b & a) | (~d & b)'<br><br>
3. ![a | ~(b & ~(a & d)) | (b & ~(b | (d & ~c)))](LogicCircuitPainter/examples/example_3.jpg)<br>
Logical Expression: 'a | ~(b & ~(a & d)) | (b & ~(b | (d & ~c)))'<br><br>
