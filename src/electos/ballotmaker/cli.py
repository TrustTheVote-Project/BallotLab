""" The BallotMaker Command Line Interface (CLI)"""
from os import strerror
from pathlib import Path
from typing import Optional

import typer
from electos.ballotmaker import make_ballots, validate_edf
from electos.ballotmaker.constants import NO_ERRORS, PROGRAM_NAME, VERSION

EDF_HELP = "EDF file with ballot data (JSON format)"
PDF_OUTPUT_HELP = "EDF file with ballot data (JSON format)"
STYLE_HELP = "Stylesheet file for ballot generation"
VERSION_HELP = "Print the version number."


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
        None, "--version", callback=version_callback, help=VERSION_HELP
    ),
):
    return NO_ERRORS


@app.command()
def make(
    edf: Path = typer.Option(
        ...,
        help=EDF_HELP,
    ),
    output_dir: Path = typer.Option(None, help=PDF_OUTPUT_HELP),
    style: Path = typer.Option(None, help=STYLE_HELP),
):
    """Make ballots from EDF file"""
    make_ballots_result = make_ballots.make_ballots(edf, output_dir, style)
    if make_ballots_result != NO_ERRORS:
        typer.echo(
            f"Error {make_ballots_result} making ballots: {strerror(make_ballots_result)}"
        )
    return make_ballots_result


@app.command()
def validate(
    edf: Path = typer.Option(
        ...,
        help=EDF_HELP,
    ),
):
    """Validate data in EDF file"""
    validate_edf_result = validate_edf.validate_edf(edf)
    if validate_edf_result != NO_ERRORS:
        typer.echo(
            f"Error {validate_edf_result} validating EDF: {strerror(validate_edf_result)}"
        )
    return validate_edf_result


if __name__ == "__main__":
    app()  # pragma: no cover
