import argparse
import collections

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

    The command is run by calling the class method Command.run(). This allows
    it to be used directly in a setuptools setup config for a command line
    script.
    """

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        d = self.__class__.__dict__
        description = d.get("__description__", None)
        self.__log = d.get("__logger__", None)

        self.parser = argparse.ArgumentParser(description=description)

        args = []

        # Now loop through the class-level definitions and find all of the
        # arguments. Currently we don't check that the variable is named in
        # a funny way (e.g. a special __x__ variable). As long as it's an
        # argument, assume the name of the variable is passable.
        for prop, value in d.items():
            if not isinstance(value, Argument):
                continue

            args.append((prop, value))

        # Order the arguments based on the order in which the instances were
        # created, which is the same as the order in which they were written
        # down in the class.
        args.sort(key=lambda x: x[1]._instance_id)
        self.args = collections.OrderedDict(args)

        for k, v in self.args.items():
            v.add_to_parser(k, self.parser)

    def parse_args(self):
        """This method parses the arguments provided on the command line. It
        is intentionally separate from __init__ to allow for a hook to be
        called before the arguments are parsed (for example, to dynamically
        add arguments - you cannot have for loops or other logic in the class
        definitions).
        """

        parsed_args = self.parser.parse_args()

        for arg in self.args:
            value = getattr(parsed_args, arg)
            value = self.args[arg].process_value(value)
            setattr(self, arg, value)

    def error(self, s="", run_exit=True, error_code=1, *args):
        """A helper method which should be called when an error occurs."""
        if self.__log:
            self.__log.error(s, *args)

        print("Error:", s * args)
        if run_exit:
            exit(error_code)

    def warning(self, s="", *args):
        """A helper method which should be called to warn the user."""
        if self.__log:
            self.__log.warning(s, *args)

        print("Warning:", s * args)

    @classmethod
    def run(cls):
        """This is the method which should be called to run the command."""
        command = cls()
        command.before_parse()
        command.parse_args()
        command.main()

    def before_parse(self):
        """Use this hook for dynamic behaviour which needs to occur before the
        arguments are parsed, e.g. adding dynamically-generated arguments."""
        pass

    def main(self):
        """This method should be overridden in subclasses of command. It
        contains the major logic that should be run when the command is run."""
        pass
