import argparse
import functools
import inspect


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__subparsers = None

    @property
    def subparsers(self):
        if self.__subparsers is None:
            self.__subparsers = self.add_subparsers()
        return self.__subparsers

    def subcommand(self, func=None, **subcommand_options):
        """
        Decorator to register a function as a subcommand.

        Example:

            @parser.subcommand(name="list")
            def list_cmd(args):
                pass

            @parser.subcommand(
                name="describe",
                args=[
                    ["item_id", {"help": "Id of item to describe}]
                ],
            )
            def describe_cmd(args):
                pass

        """

        def decorator(subcommand_func):
            subcommand_sig = inspect.signature(subcommand_func)

            @functools.wraps(subcommand_func)
            def wrapped(args):

                final_args = []
                final_kwargs = {}

                if "args" in subcommand_sig.parameters:
                    final_kwargs["args"] = args

                return subcommand_func(*final_args, **final_kwargs)

            subcommand_name = subcommand_options.pop("name", subcommand_func.__name__)
            subcommand_args_def = subcommand_options.pop("args", None) or ()
            subcommand_doc = subcommand_options.pop("help", None) or subcommand_options.pop("description", None)
            if subcommand_doc is None:
                subcommand_doc = subcommand_func.__doc__
            subcommand_aliases = subcommand_options.pop("aliases", None) or []
            if subcommand_options:
                raise ValueError(f"Unexpected kwarg(s): {', '.join(str(k) for k in subcommand_options.keys())}")

            parser = self.subparsers.add_parser(
                name=subcommand_name,
                help=subcommand_doc,
                description=subcommand_doc,
                aliases=subcommand_aliases,
            )
            parser.set_defaults(func=wrapped)

            for arg in subcommand_args_def:
                if isinstance(arg, str):
                    parser.add_argument(arg)
                elif isinstance(arg, (list, tuple)):
                    if isinstance(arg[-1], dict):
                        arg_args = arg[:-1]
                        arg_kwargs = arg[-1]
                    else:
                        arg_args = arg[:]
                        arg_kwargs = {}
                    parser.add_argument(*arg_args, **arg_kwargs)
                else:
                    raise TypeError(r"Expected a string or list, got {arg!r}")

            return parser

        if func is None:
            return decorator
        else:
            return decorator(func)
