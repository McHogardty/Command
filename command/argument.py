

class Argument(object):
    """This class represents an argument or set of arguments to a command line
    program."""
    # The argparse string specifying how many arguments should be collected.
    nargs = ""
    # If the argument is not specified, it will resort to this default.
    default = ""
    # If an argument is positional, it is specified without the - or -- syntax
    # or an option string.
    positional = False

    def __init__(self, nargs="", default="", help="", positional=None):
        # The self.x = x or self.x pattern allows us to set defaults using
        # class variables. Note that if the instance does not have the property
        # x set, then python magically looks to the class variables for one
        # named x. Thus, we should always set self.x = self.x even without a
        # kwarg so that the instance stores its own state rather than always
        # looking at the class variables (which should essentially be
        # "immutable").
        self.nargs = nargs or self.nargs
        self.default = default or self.default
        self.help = help

        # The positional kwarg always overrides the class variable.
        if positional is not None:
            self.positional = positional
        else:
            self.positional = self.positional

    def add_to_parser(self, name, parser):
        if not self.positional:
            name = "--" + name

        parser.add_argument(name, help=self.help)
