from pathlib import Path

from electos.ballotmaker.constants import NO_ERRORS, NO_FILE


def validate_edf(
    _edf: Path,
) -> int:
    """Validate EDF data
    Requires:
        EDF file (JSON format) edf_file: Path,
    """
    # is the EDF a JSON file?
    # if _edf is None:
    #     return NO_FILE
    return NO_ERRORS
