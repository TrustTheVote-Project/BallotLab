import json
import logging
from dataclasses import asdict
from pathlib import Path

from electos.ballotmaker.constants import NO_ERRORS
from electos.ballotmaker.data.extractor import BallotDataExtractor

log = logging.getLogger(__name__)


def report(data, **opts):
    """Generate data needed by BallotLab."""
    extractor = BallotDataExtractor()
    ballot_data = extractor.extract(data)
    ballot_data = [asdict(_) for _ in ballot_data]
    print(json.dumps(ballot_data, indent=4))


def validate_edf(
    _edf: Path,
) -> int:
    """Validate EDF data
    Requires:
        EDF file (JSON format) edf_file: Path,
    """
    with _edf.open() as input:
        text = input.read()
        data = json.loads(text)
        report(data)
    return NO_ERRORS
