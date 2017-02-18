import threading


class Argument(object):
    """This class represents an argument or set of arguments to a command line
    program.

    An Argument implements two methods: add_to_parser(self, name, parser) and
    process_value(self, value). add_to_parser is called when the argument needs
    to be added to the argparse.Parser. process_value is called after the value
    is parsed to allow for custom processing of the value.
    """

    # The argparse string specifying how many arguments should be collected.
    nargs = ""
    # If the argument is not specified, it will resort to this default.
    default = ""
    # If an argument is positional, it is specified without the - or -- syntax
    # or an option string. By default arguments are not positional.
    positional = False
    # If an argument is required then it must be specified. Typically
    # positional arguments are always required because it would be impossible
    # to parse positional arguments if they were all optional.
    required = False
    # validator is a function which takes the value from the command line and
    # tries to coerce it to a desired type. It returns ValueError if there is
    # a problem.
    validator = None
    # If multiple is true, then one or more arguments may be parsed from the
    # command line and collected into a python list.
    multiple = False
    # Contains the possible values which can be provided for this argument.
    choices = None

    _creation_counter = threading.Lock()
    _instance_count = 0

    def __init__(self, nargs="", default="", help="", positional=None,
                 required=False, validator=None, multiple=False, choices=None):
        # The self.x = x or self.x pattern allows us to set defaults using
        # class variables. Note that if the instance does not have the property
        # x set, then python magically looks to the class variables for one
        # named x. Thus, we should always set self.x = self.x even without a
        # kwarg so that the instance stores its own state rather than always
        # looking at the class variables (which should essentially be
        # "immutable").
        self.nargs = nargs or self.nargs
        self.default = default or self.default
        self.required = required or self.required
        self.validator = validator or self.validator
        self.multiple = multiple or self.multiple
        self.choices = choices or self.choices
        self.help = help

        # The positional kwarg always overrides the class variable.
        if positional is not None:
            self.positional = positional
        else:
            self.positional = self.positional

        with self._creation_counter:
            self._instance_id = Argument._instance_count
            Argument._instance_count += 1

    def add_to_parser(self, name, parser):
        if not self.positional:
            name = "--" + name

        kwargs = {
            "help": self.help,
            "default": self.default,
            "type": self.validator,
            "choices": self.choices,
        }

        if self.multiple:
            kwargs["nargs"] = "+" if self.required else "*"
        elif self.positional and not self.required:
            kwargs["nargs"] = "?"

        parser.add_argument(name, **kwargs)

    def process_value(self, value):
        if self.multiple and not value:
            return []

        return value
