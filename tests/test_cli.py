from typer.testing import CliRunner
from electos.ballotmaker import cli
from electos.ballotmaker.constants import NO_ERRORS, PROGRAM_NAME, VERSION

runner = CliRunner()


# def test_version_string():
#     assert __version__.__version__ == "0.1.0"


def test_main():
    assert cli.main() == NO_ERRORS


# does Usage help appear with no options?
def test_usage():
    result = runner.invoke(cli.app)
    assert result.exit_code == NO_ERRORS
    assert "Usage:" in result.stdout


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == NO_ERRORS
    assert f"{PROGRAM_NAME} version: {VERSION}" in result.stdout


def test_make():
    assert cli.make() == NO_ERRORS
