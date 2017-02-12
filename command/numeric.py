from .argument import Argument


class Integer(Argument):
    validator = staticmethod(int)
