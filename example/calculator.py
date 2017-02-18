from command import Command, Integer


class Operation(Command):
    first = Integer(positional=True, required=True,
                    help="The first number.")
    second = Integer(positional=True, required=True,
                     help="The second number.")


class Add(Operation):
    __description__ = "Add together two numbers."

    def main(self):
        print(self.first + self.second)


class Subtract(Operation):
    __description__ = "Find the difference of two numbers."

    def main(self):
        print(self.first - self.second)


class Multiply(Operation):
    __description__ = "Multiply two numbers."

    def main(self):
        print(self.first * self.second)


class Divide(Operation):
    __description__ = "Divide two numbers."

    def main(self):
        print(self.first / self.second)


class Calculator(Command):
    __description__ = ("This program adds together numbers provided on the "
                       "command line.")

    __subcommand_name__ = "operation"

    add = Add
    subtract = Subtract
    multiply = Multiply
    divide = Divide


if __name__ == "__main__":
    Calculator.run()
