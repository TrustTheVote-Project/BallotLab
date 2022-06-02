""" The BallotMaker Command Line Interface (CLI)"""

from typing import Optional

import typer

## execute with 'python -m' to find this module
from src.electos.ballotmaker import __version__

PROGRAM_NAME = "BallotMaker"

# for this to work, main needs to be a callback, not a command
app = typer.Typer(no_args_is_help=True)


@app.command()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", help="Print the version number."
    ),
):
    """Create ballot PDFs from an Election Data File (EDF)"""
    if version:
        typer.echo(f"{PROGRAM_NAME} version: {__version__.__version__}")
        raise typer.Exit()


if __name__ == "__main__":
    app()
