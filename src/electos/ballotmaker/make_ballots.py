"""Generate ballots from EDF data
    Requires: 
        EDF file (JSON format) edf_file: Path, 
    Optional:
        Output directory for generated PDF files
        Settings file for ballot generation
"""
from pathlib import Path
from electos.ballotmaker.constants import NO_ERRORS


def make_ballots(
    _edf: Path = None, _output_dir: Path = None, _settings: Path = None
) -> int:
    # is the EDF a JSON file?
    # was a valid output directory provided?
    # was a settings file provided?
    return NO_ERRORS
