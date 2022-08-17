import logging
from pathlib import Path

from electos.ballotmaker.election_data import ElectionData

log = logging.getLogger(__name__)


def validate_edf(
    _edf: Path,
) -> int:
    """Validate EDF data
    Requires:
        EDF file (JSON format) edf_file: Path,
    """
    election_data = ElectionData(_edf)

    return election_data.edf_error
