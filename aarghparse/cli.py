import functools
from typing import Callable, Type

from .func_utils import optional_args_func
from .parsers import ArgumentParser


def cli(init_parser: Callable) -> Type["Cli"]:
    """
    Decorator for a function that takes "parser: ArgumentParser" as argument and initialises it as required.
    """

    cli_help = init_parser.__doc__
    init_parser = optional_args_func(init_parser)

    class CustomCli(Cli):
        def __init__(self):
            super().__init__()
            self.parser.description = cli_help
            init_parser(parser=self.parser, subcommand=self.parser.subcommand)

    CustomCli.__name__ = init_parser.__name__
    CustomCli.__qualname__ = init_parser.__qualname__

    return CustomCli


class _WithInstance:
    """
    This allows the method to be called with a class as well as with instance.
    If called with a class it will create a new instance and return a method
    bound to that instance.
    """

    def __init__(self, method):
        self.method = method

    def __set_name__(self, owner, name):
        self.__name__ = name

    def __get__(self, instance, owner):
        if instance is None:
            instance = owner()
        return functools.partial(self.method, instance)


class Cli:
    parser: ArgumentParser

    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.set_defaults(func=optional_args_func(self.parser.print_help))

    def _run(self, args=None):
        parsed_args = self.parser.parse_args(args=args)
        parsed_args.func(args=parsed_args)

    run: Callable = _WithInstance(_run)
