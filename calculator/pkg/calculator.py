class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    # validate expression, remove whitespace and split expression into individual pieces
    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        values = []  # stores numerical values from expression
        operators = []  # stores mathematical operators

        for token in tokens:
            if token in self.operators:
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"invalid token: {token}")

        while operators:
            self._apply_operator(operators, values)

        # after calculations values should have only one value i.e. final answer
        if len(values) != 1:
            raise ValueError("invalid expression")

        # return final answer
        return values[0]

    def _apply_operator(self, operators, values):
        # checks if operators list is empty
        if not operators:
            return

        operator = operators.pop()
        # checks if there are enough operands
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        b = values.pop()
        a = values.pop()
        """
        passes a, b to lambda function of operator's key
        appends result to values
        """
        values.append(self.operators[operator](a, b))
