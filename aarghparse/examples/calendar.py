import datetime as dt

import dateutil.tz

from aarghparse import ArgumentParser, arg_converter, cli


@cli
def calendar_cli(parser: ArgumentParser, subcommand: ArgumentParser.subcommand):
    """
    Command-line calendar.
    """

    parser.add_argument(
        '--date-format',
        default=None,
    )

    @arg_converter
    def tz_arg(value):
        return dateutil.tz.gettz(value)

    @subcommand(
        name="now",
        args=[
            ["--tz", {
                "action": tz_arg,
                "help": "Timezone",
            }],
        ],
    )
    def now_cmd(args):
        """
        Prints today's date.
        """
        date_format = args.date_format or "%Y-%m-%d %H:%M:%S"
        print(dt.datetime.now(tz=args.tz).strftime(date_format))


if __name__ == "__main__":
    calendar_cli()
