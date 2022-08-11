import logging
from pathlib import Path

from electos.ballotmaker.constants import NO_DATA, NO_ERRORS, NO_FILE
from electos.ballotmaker.read_edf import read_edf

log = logging.getLogger(__name__)


def validate_edf(
    _edf: Path,
) -> int:
    """Validate EDF data
    Requires:
        EDF file (JSON format) edf_file: Path,
    """
    # is the EDF a file?
    if _edf is None:
        log.debug("No EDF file provided.")
        return NO_FILE
    if Path.is_file(_edf) is False:
        log.debug(f"{_edf} is not a file")
        return NO_FILE

    ballot_style_count = read_edf(_edf)
    log.info(f"Found {ballot_style_count} ballots in {_edf}")
    return NO_ERRORS
