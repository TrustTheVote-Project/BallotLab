import json
from pathlib import Path

from electos.datamodels.nist.indexes import ElementIndex
from electos.datamodels.nist.models.edf import ElectionReport


def read_edf(path_to_edf: Path) -> int:
    """Opens the specified EDF file, returns the number of BallotStyles"""
    edf_data = json.loads(path_to_edf.read_text())
    election_report = ElectionReport(**edf_data)
    index = ElementIndex(election_report, "ElectionResults")
    ballot_styles = index.by_type("ElectionResults.BallotStyle")
    return sum(1 for _ in ballot_styles)
