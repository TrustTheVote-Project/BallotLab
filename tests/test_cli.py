from typer.testing import CliRunner
from electos.ballotmaker import cli
from electos.ballotmaker.constants import NO_ERRORS, VERSION

runner = CliRunner()


# def test_version_string():
#     assert __version__.__version__ == "0.1.0"


def test_main():
    assert cli.main() == NO_ERRORS


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == NO_ERRORS
    assert f"version: {VERSION}" in result.stdout


def test_make():
    assert cli.make() == NO_ERRORS
