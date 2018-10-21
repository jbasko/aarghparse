import argparse
import inspect


def arg_converter(func=None, **options):
    """
    Decorator to declare simple argparse argument value converters without argparse.Action boilerplate

    Example:

        @arg_converter
        def int_value(value):
            return int(value)

        parser.add_argument('x', action=int_value)

    """

    def decorator(converter_func):
        sig = inspect.signature(converter_func)

        def action_func(action, parser, args, value, option_string=None):
            all_args = {
                'action': action,
                'parser': parser,
                'args': args,
                'value': value,
                'option_string': option_string,
            }
            converter_args = {k: all_args[k] for k in sig.parameters}
            setattr(args, action.dest, converter_func(**converter_args))

        if hasattr(func, "__name__"):
            name = getattr(func, "__name__")
        else:
            name = func.__class__.__name__

        return type(
            '{}#argparse.Action'.format(name),
            (argparse.Action,),
            {'__call__': action_func}
        )

    if func is None:
        return decorator
    else:
        return decorator(func)
