OPERATIONS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}


def calculate(a: float, operator: str, b: float) -> float:
    if operator not in OPERATIONS:
        raise ValueError(f"Unsupported operator: {operator}")
    if operator == "/" and b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return OPERATIONS[operator](a, b)
