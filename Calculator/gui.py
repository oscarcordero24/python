import tkinter as tk

from calculator import calculate

BUTTON_LAYOUT = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["C", "0", "=", "+"],
]

OPERATORS = ("+", "-", "*", "/")


class CalculatorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)

        self.expression = ""

        self.display_var = tk.StringVar(value="0")
        display = tk.Entry(
            root,
            textvariable=self.display_var,
            font=("Arial", 24),
            justify="right",
            state="readonly",
            readonlybackground="white",
            bd=10,
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        for row_index, row in enumerate(BUTTON_LAYOUT, start=1):
            for col_index, label in enumerate(row):
                button = tk.Button(
                    root,
                    text=label,
                    font=("Arial", 18),
                    command=lambda label=label: self.on_button_press(label),
                )
                button.grid(row=row_index, column=col_index, sticky="nsew", padx=2, pady=2)

        for i in range(4):
            root.grid_columnconfigure(i, weight=1)
        for i in range(len(BUTTON_LAYOUT) + 1):
            root.grid_rowconfigure(i, weight=1)

    def on_button_press(self, label: str):
        if label == "C":
            self.expression = ""
        elif label == "=":
            self.evaluate()
            return
        else:
            self.expression += label

        self.display_var.set(self.expression if self.expression else "0")

    def evaluate(self):
        operator = next((op for op in OPERATORS if op in self.expression[1:]), None)
        if operator is None:
            return

        operator_index = self.expression.index(operator, 1)
        left = self.expression[:operator_index]
        right = self.expression[operator_index + 1:]

        try:
            result = calculate(float(left), operator, float(right))
            self.display_var.set(str(result))
            self.expression = str(result)
        except (ValueError, ZeroDivisionError) as e:
            self.display_var.set(f"Error: {e}")
            self.expression = ""


def main():
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
