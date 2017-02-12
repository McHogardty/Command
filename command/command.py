import argparse

from .argument import Argument


class Command(object):
    """The base class for a command-line program. It allows for a declarative-
    style syntax for quickly and simply creating python programs. At the
    moment it is essentially a wrapper around the argparse module.

    Arguments are defined as class variables, each of which is set to an
    instance of a subclass of command.Argument.

    There are also some metavariables which use the double underscore syntax.
    They are:
    - __description__: a human-readable description of what the program does.
    - __logger__: a logging object for logging of errors and warnings.

    The command is run by calling the class method Command.run. This allows it
    to be used directly in a setuptools setup config.
    """

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        d = self.__class__.__dict__
        description = d.get("__description__", None)

        self.parser = argparse.ArgumentParser(description=description)
        self.args = args = []

        # Now loop through the class-level definitions and find all of the
        # arguments. Currently we don't check that the variable is named in
        # a funny way (e.g. a special __x__ variable). As long as it's an
        # argument, assume the name of the variable is passable.
        for prop, value in d.items():
            if not isinstance(value, Argument):
                continue

            value.add_to_parser(prop, self.parser)
            self.args.append(prop)

    def parse_args(self):
        """This method parses the arguments provided on the command line. It
        is intentionally separate from __init__ to allow for a hook to be
        called before the arguments are parsed (for example, to dynamically
        add arguments - you cannot have for loops or other logic in the class
        definitions).
        """

        parsed_args = self.parser.parse_args()

        for arg in self.args:
            setattr(self, arg, getattr(parsed_args, arg))

    @classmethod
    def run(cls):
        command = cls()
        command.parse_args()
        command.main()

    def main(self):
        pass
