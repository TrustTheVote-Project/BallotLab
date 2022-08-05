from pathlib import Path

from electos.ballotmaker.constants import NO_ERRORS, NO_FILE


def make_ballots(
    _edf: Path, _output_dir: Path = None, _styles: Path = None
) -> int:
    """Generate ballots from EDF data
    Requires:
        EDF file (JSON format) edf_file: Path,
    Optional:
        Output directory for generated PDF files
        Styles file for ballot formatting
    """
    # is the EDF a JSON file?
    if _edf is None:
        return NO_FILE
    # was a valid output directory provided?
    # was a styles file provided?
    return NO_ERRORS
