""" The BallotMaker Command Line Interface (CLI)"""
from pathlib import Path
from typing import Optional
import typer

from electos.ballotmaker import make_ballots
from electos.ballotmaker.constants import NO_ERRORS, VERSION, PROGRAM_NAME


def version_callback(value: bool):
    if value:
        typer.echo(f"{PROGRAM_NAME} version: {VERSION}")
        raise typer.Exit()


# to display help when no arguments are provided,
# main needs to be a callback, not a command
app = typer.Typer(no_args_is_help=True)


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, help="Print the version number."
    ),
):
    return NO_ERRORS


@app.command()
def make(
    edf: Path = typer.Option(
        ...,
        help="EDF file with ballot data (JSON format)",
    ),
    output_dir: Path = typer.Option(
        None, help="Output directory for generated PDFs (default: your home directory"
    ),
    settings: Path = typer.Option(None, help="Settings file for ballot generation"),
):
    """Make ballots from EDF file"""
    make_ballots_result = make_ballots.make_ballots(edf, output_dir, settings)
    # if make_ballots_result != NO_ERRORS:
    #     typer.echo(f"Error: {make_ballots_result}")
    return make_ballots_result


if __name__ == "__main__":
    app()  # pragma: no cover
