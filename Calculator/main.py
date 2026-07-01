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


def main():
    print("Simple Calculator")
    print(f"Supported operators: {', '.join(OPERATIONS)}")
    print("Enter 'q' to quit.\n")

    while True:
        expression = input("Enter expression (e.g. 3 + 4): ").strip()
        if expression.lower() == "q":
            break

        parts = expression.split()
        if len(parts) != 3:
            print("Invalid format. Use: <number> <operator> <number>\n")
            continue

        num1_str, operator, num2_str = parts
        try:
            num1 = float(num1_str)
            num2 = float(num2_str)
            result = calculate(num1, operator, num2)
            print(f"Result: {result}\n")
        except ValueError as e:
            print(f"Error: {e}\n")
        except ZeroDivisionError as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
