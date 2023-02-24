import tkinter as tk

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")

        # Create input fields
        self.num1_var = tk.StringVar()
        self.num2_var = tk.StringVar()
        self.operator_var = tk.StringVar()

        # Create input labels
        tk.Label(master, text="Number 1:").grid(row=0, column=0)
        tk.Label(master, text="Number 2:").grid(row=1, column=0)
        tk.Label(master, text="Operator:").grid(row=2, column=0)

        # Create input entries
        tk.Entry(master, textvariable=self.num1_var).grid(row=0, column=1)
        tk.Entry(master, textvariable=self.num2_var).grid(row=1, column=1)
        tk.Entry(master, textvariable=self.operator_var).grid(row=2, column=1)

        # Create calculate button
        tk.Button(master, text="Calculate", command=self.calculate).grid(row=3, column=1)

        # Create result label
        self.result_var = tk.StringVar()
        tk.Label(master, textvariable=self.result_var).grid(row=4, column=1)

    def calculate(self):
        num1 = float(self.num1_var.get())
        num2 = float(self.num2_var.get())
        operator = self.operator_var.get()

        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            result = num1 / num2
        else:
            result = "Invalid operator"

        self.result_var.set(result)

root = tk.Tk()
calculator = Calculator(root)
root.mainloop()
