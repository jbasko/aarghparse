import pytest

from aarghparse import cli
from aarghparse.cli import Cli


def test_cli_returns_class():
    @cli
    def my_cli():
        pass

    assert isinstance(my_cli, type)
    assert issubclass(my_cli, Cli)
    assert my_cli.__name__ == "my_cli"


def test_cli_runnable_with_class_and_instance():
    @cli
    def my_cli():
        pass

    with pytest.raises(SystemExit) as exc_info:
        my_cli.run(args=['--help'])
    assert exc_info.value.code == 0

    with pytest.raises(SystemExit) as exc_info:
        my_cli().run(args=['--help'])
    assert exc_info.value.code == 0


def test_cli_init_parser_accepts_named_args():
    kwargs_seen = []

    @cli
    def my_cli(a, b, parser):
        parser.add_argument('-x')
        kwargs_seen.append((a, b))

    my_cli(a=1, b=2)

    assert kwargs_seen[0] == (1, 2)
