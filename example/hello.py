from command import Argument, Command


class HelloWorld(Command):
    __description__ = ("This program says hello to whomever you want. If no "
                       "argument is provided, it will say hello to everybody.")

    name = Argument(positional=True)

    def main(self):
        print("Hello, {0}!".format(self.name))


if __name__ == "__main__":
    HelloWorld.run()
