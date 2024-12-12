import sympy as sp
import networkx as nx

expr = input("Enter an expression: ")
try:
    expr = sp.sympify(expr)
    print(expr)
except sp.SympifyError as e:
    print(f"Error while parsing expression: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
