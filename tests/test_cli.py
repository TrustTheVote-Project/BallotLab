from electos.ballotmaker.make_ballots import NO_ERRORS
from typer.testing import CliRunner
from electos.ballotmaker import __version__, cli
from electos.ballotmaker.constants import NO_ERRORS

runner = CliRunner()


# def test_version_string():
#     assert __version__.__version__ == "0.1.0"


def test_main():
    main_result = cli.main()
    assert main_result == NO_ERRORS


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"version: {__version__.__version__}" in result.stdout


def test_make():
    make_result = cli.make()
    assert make_result == NO_ERRORS
