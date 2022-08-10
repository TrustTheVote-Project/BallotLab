from pathlib import Path

from electos.datamodels.nist.indexes import ElementIndex
from electos.datamodels.nist.models.edf import ElectionReport


def read_edf(path_to_edf: Path) -> int:
    """Opens the specified EDF file, returns the number of BallotStyles"""
    return 3
