from typing import Dict

class Services:

    def apply_operators(operators, values):
        operator = operators.pop()
        value_2 = values.pop()
        value_1 = values.pop()
        if operator == "+":
            values.append(value_1 + value_2)
        elif operator == "-":
            values.append(value_1 - value_2)
        elif operator == "*":
            values.append(value_1 * value_2)
        elif operator == "/":
            values.append(value_1 / value_2)


    def operator_priority(operator: str) -> int:
        if operator in ("+", "-"):
            return 1
        if operator in ("*", "/"):
            return 2
        return 0

    def calculate_infix_operation(self, expression: str) -> Dict[str, str]:
        operators = []
        values = []
        i = 0

        while i < len(expression):
            if expression[i] == " ":
                i += 1
                continue
            elif expression[i] == "(":
                operators.append("(")
            elif expression[i].isdigit():
                value = 0
                while i < len(expression) and expression[i].isdigit():
                    value = (value * 10) + int(expression[i])
                    i += 1
                values.append(value)
                i -= 1
            elif expression[i] == ")":
                while operators and operators[-1] != "(":
                    self.apply_operators(operators, values)
                operators.pop()
            else:
                while (operators and self.operator_priority(operators[-1]) >= self.operator_priority(expression[i])):
                    self.apply_operators(operators, values)
                operators.append(expression[i])
            i += 1

        while operators:
            self.apply_operators(operators, values)

        return {"operation": expression, "result": str(values[-1])}
    
    def calculate_postfix_operation(expression: str) -> float:
        pile = []
        for element in expression:
            if element.isdigit():
                pile.append(int(element))
            else:
                value_2 = pile.pop()
                value_1 = pile.pop()

            if element == "+":
                result = value_1 + value_2
                pile.append(result)
            elif element == "-":
                result = value_1 - value_2
                pile.append(result)
            elif element == "*":
                result = value_1 * value_2
                pile.append(result)
            elif element == "/":
                result = value_1 / value_2
                pile.append(result)

        return {"operation": expression, "result": str(pile.pop())}