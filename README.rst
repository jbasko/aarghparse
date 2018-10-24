==========
aarghparse
==========

Motivation
----------

I was having shower and this name came up.

At the moment this is a collection of `argparse`_ extensions I have written and found useful in recent times.

..
    But really I want an ``argparse``-based argument parser which is able to load plugins based on parsed arguments
    and let those plugins define additional arguments. I have made this work for one of my clients, but it's dirty.


Features
--------

* ``@arg_converter`` decorator to write simple argument value parsers without the ``argparse.Action`` boilerplate
* ``@subcommand`` decorator to save you from all the ``add_subparsers`` and ``set_defaults(func=)``.
* ``@cli`` decorator to generate a command-line interface.


..
    The dynamic loader mentioned in the Motivation_ isn't available yet.


.. _argparse: https://docs.python.org/3/library/argparse.html


Example
-------

The example below combines all the features, but the tool doesn't enforce it on you.

If you have an existing ``argparse.ArgumentParser`` definition, you should be able to replace it with ``aarghparse``
by just changing the initialisation line to ``parser = aarghparse.ArgumentParser(...)``.

.. code-block:: python

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
        calendar_cli.run()


If you install ``python-dateutil`` then you can try the above with:

.. code-block:: shell

    python -m aarghparse.examples.calendar --help
    python -m aarghparse.examples.calendar now --help
    python -m aarghparse.examples.calendar now --tz "Europe/Riga"
    python -m aarghparse.examples.calendar --date-format "%d.%m.%Y." now --tz "Europe/Riga"

