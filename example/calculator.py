from command import Command, Integer


class Calculator(Command):
    __description__ = ("This program adds together numbers provided on the"
                       "command line.")

    numbers = Integer(positional=True, multiple=True, required=True)

    def main(self):
        print(sum(self.numbers))


if __name__ == "__main__":
    Calculator.run()
