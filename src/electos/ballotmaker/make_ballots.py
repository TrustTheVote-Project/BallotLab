import logging
from pathlib import Path

from electos.ballotmaker.election_data import ElectionData

log = logging.getLogger(__name__)


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
    # was a valid output directory provided?
    # was a styles file provided
    election_data = ElectionData(_edf)
    return election_data.edf_error
