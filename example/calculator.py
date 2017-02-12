from command import Argument, Command, Integer


# These variables are used to represent the mathematical operations.
ADD = "add"
SUBTRACT = "subtract"
MULTIPLY = "multiply"
DIVIDE = "divide"


class Calculator(Command):
    __description__ = ("This program adds together numbers provided on the"
                       "command line.")

    operation = Argument(positional=True, required=True,
                         choices=[ADD, SUBTRACT, MULTIPLY, DIVIDE],
                         help="The operation to perform on the numbers.")
    first = Integer(positional=True, required=True,
                    help="The first number.")
    second = Integer(positional=True, required=True,
                     help="The second number.")

    def main(self):
        if self.operation == ADD:
            print(self.first + self.second)
        elif self.operation == SUBTRACT:
            print(self.first - self.second)
        elif self.operation == MULTIPLY:
            print(self.first * self.second)
        elif self.operation == DIVIDE:
            print(self.first / self.second)


if __name__ == "__main__":
    Calculator.run()
