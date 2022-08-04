from pathlib import Path

from electos.ballotmaker import cli
from electos.ballotmaker.constants import (
    NO_ERRORS,
    NO_FILE,
    PROGRAM_NAME,
    VERSION,
)
from typer.testing import CliRunner

runner = CliRunner()
imaginary_file = Path("not_a_file.txt")


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
    # bypass mandatory CLI option to force error
    assert cli.make(edf=None) == NO_FILE
    # any old path will satisfy current tests
    assert cli.make(imaginary_file) == NO_ERRORS
