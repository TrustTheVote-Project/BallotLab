""" The BallotMaker Command Line Interface (CLI)"""
import logging
import sys
from os import strerror
from pathlib import Path
from typing import Optional

import typer
from electos.ballotmaker import make_ballots, validate_edf
from electos.ballotmaker.ballots.demo_ballot import build_ballot
from electos.ballotmaker.constants import NO_ERRORS, PROGRAM_NAME, VERSION

EDF_HELP = "EDF file with ballot data (JSON format)"
PDF_OUTPUT_HELP = "EDF file with ballot data (JSON format)"
STYLE_HELP = "Stylesheet file for ballot generation"
VERSION_HELP = "Print the version number."

# configure logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)


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
def demo():
    """Make ballots from previously extracted EDF data"""
    new_ballot_name = build_ballot()
    typer.echo(f"Ballot created: {new_ballot_name}")
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
        log.error(
            f"Code {make_ballots_result} in make - {strerror(make_ballots_result)}"
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
        log.error(
            f"Code {validate_edf_result} in validate - {strerror(validate_edf_result)}"
        )
    return validate_edf_result


if __name__ == "__main__":
    app()  # pragma: no cover
