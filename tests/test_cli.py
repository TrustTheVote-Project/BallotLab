from typer.testing import CliRunner
from src.electos.ballotmaker import __version__, cli

runner = CliRunner()


def test_version_string():
    assert __version__.__version__ == "0.1.0"


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"version: {__version__.__version__}" in result.stdout
