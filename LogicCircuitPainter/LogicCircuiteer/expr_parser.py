import sympy as sp


class ExprParser:
    def __init__(self, in_expr=None):
        self.in_expr = in_expr
        self.expr = sp.Expr
        self.postfix_expr = []

    def parse(self):
        try:
            self.expr = sp.parse_expr(self.in_expr)
            self.postfix_expr = self.convert_to_postfix()
        except Exception:
            raise Exception

    def convert_to_postfix(self, expression=None):
        '''
        recursive function to convert the expression to a postfix expression

        :return: list of postfix expression
        '''
        if expression is None:
            expression = self.expr

        if expression.is_Atom:
            return [str(expression)]
        elif isinstance(expression, sp.Not):
            return self.convert_to_postfix(expression.args[0]) + ["~"]
        elif isinstance(expression, sp.Or):
            return sum((self.convert_to_postfix(arg) for arg in expression.args), []) + ["|"] * (
                        len(expression.args) - 1)
        elif isinstance(expression, sp.And):
            return sum((self.convert_to_postfix(arg) for arg in expression.args), []) + ["&"] * (
                        len(expression.args) - 1)
        elif isinstance(expression, sp.Xor):
            return sum((self.convert_to_postfix(arg) for arg in expression.args), []) + ["^"] * (
                        len(expression.args) - 1)
