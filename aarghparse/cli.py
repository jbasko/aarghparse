from typing import Callable

from .func_utils import optional_args_func
from .parsers import ArgumentParser


def cli(init_parser: Callable) -> "Cli":
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

    return CustomCli()


class Cli:
    parser: ArgumentParser

    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.set_defaults(func=optional_args_func(self.parser.print_help))

    def run(self, args=None):
        parsed_args = self.parser.parse_args(args=args)
        parsed_args.func(args=parsed_args)

    def __call__(self, args=None):
        self.run(args=args)
