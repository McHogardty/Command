import argparse
import collections
import inspect

from .argument import Argument


class Command(object):
    """The base class for a command-line program. It allows for a declarative-
    style syntax for quickly and simply creating python programs. At the
    moment it is essentially a wrapper around the argparse module. Subclasses
    of Command will automatically include arguments defined on parent classes
    (unless overridden).

    Arguments are defined as class variables, each of which is set to an
    instance of a subclass of command.Argument.

    There are also some metavariables which use the double underscore syntax.
    They are:
    - __description__: a human-readable description of what the program does.
    - __logger__: a logging object for logging of errors and warnings.

    Subcommands are defined by assigning subclasses of Command to class
    variables. The class variable will be used as the name of the subcommand.

    The command is run by calling the class method Command.run(). This allows
    it to be used directly in a setuptools setup config for a command line
    script.
    """

    def __init__(self, *args, **kwargs):
        d = self.__class__.__dict__
        self._description = d.get("__description__", None)
        self._log = d.get("__logger__", None)
        self._selected_command = None
        self._subcommand_name = d.get("__subcommand_name__", "command")

        args = []
        subcommands = []

        # Now loop through the class-level definitions and find all of the
        # arguments and subcommands. We look at every class in the inheritance
        # tree as class variables in super classes are not added to the
        # __dict__ of a subclass.
        # Currently we don't check that the variable is named in a funny way
        # (e.g. a special __x__ variable). As long as it's an argument or a
        # command, assume the name of the variable is passable.
        for cls in self.__class__.mro():
            if not issubclass(cls, Command):
                continue

            for prop, value in cls.__dict__.items():
                if isinstance(value, Argument):
                    args.append((prop, value))
                elif inspect.isclass(value) and issubclass(value, Command):
                    subcommands.append((prop, value))

        # Order the arguments based on the order in which the instances were
        # created, which is the same as the order in which they were written
        # down in the class.
        args.sort(key=lambda x: x[1]._instance_id)
        self.args = collections.OrderedDict(args)
        self.subcommands = collections.OrderedDict(subcommands)

    def add_to_parser(self, parser):
        """This method is called with an argparse parser object as the sole
        argument. The command should add its arguments to the parser, including
        subcommands."""
        if self.subcommands:
            subparsers = parser.add_subparsers(metavar=self._subcommand_name,
                                               dest="__subparser__")
            subparsers.required = not self.args

            for name, subcommand in self.subcommands.items():
                subcommand = subcommand()
                subparser = subparsers.add_parser(
                    name,
                    help=subcommand._description
                )
                subcommand.add_to_parser(subparser)

        for k, v in self.args.items():
            v.add_to_parser(k, parser)

    def get_args(self, parsed_args):
        """This method is called after the arguments are parsed. The command
        should get the relevant arguments."""

        for arg in self._selected_command.args:
            value = getattr(parsed_args, arg, None)
            value = self._selected_command.args[arg].process_value(value)
            setattr(self._selected_command, arg, value)

    def parse_args(self):
        """This method parses the arguments provided on the command line. It
        is intentionally separate from __init__ to allow for a hook to be
        called before the arguments are parsed (for example, to dynamically
        add arguments - you cannot have for loops or other logic in the class
        definitions)."""

        parser = argparse.ArgumentParser(description=self._description)

        self.add_to_parser(parser)

        parsed_args = parser.parse_args()

        self._selected_command = self
        if self.subcommands:
            subparser = parsed_args.__subparser__

            if subparser:
                self._selected_command = self.subcommands[subparser]()

        self.get_args(parsed_args)

    def error(self, *args, **kwargs):
        """A helper method which should be called when an error occurs.
        The first argument should be a format string, followed by the format
        arguments.

        It takes the following kwargs:
        - run_exit: Whether or not to exit after logging the error.
        - error_code: the code to be passed to the system exit function.
        """

        # args should be a tuple, with the first argument a format string
        # and the rest of the arguments the format args.
        s = args[0]
        args = args[1:]
        if self._log:
            self._log.error(s, *args)

        print("Error:", s % args)
        if kwargs.get("run_exit", True):
            exit(kwargs.get("error_code", 1))

    def warning(self, *args, **kwargs):
        """A helper method which should be called to warn the user."""

        # warning works the same way as error
        s = args[0]
        args = args[1:]
        if self._log:
            self._log.warning(s, *args)

        print("Warning:", s % args)

    def _run(self):
        self._selected_command.main()

    @classmethod
    def run(cls):
        """This is the method which should be called to run the command."""
        command = cls()
        command.before_parse()
        command.parse_args()
        command._run()

    def before_parse(self):
        """Use this hook for dynamic behaviour which needs to occur before the
        arguments are parsed, e.g. adding dynamically-generated arguments."""
        pass

    def main(self):
        """This method should be overridden in subclasses of command. It
        contains the major logic that should be run when the command is run."""
        pass
