from pathlib import Path

from electos.ballotmaker import validate_edf
from electos.ballotmaker.constants import NO_ERRORS, NO_FILE

test_file = Path("empty.json")


def test_validate_edf():
    # force a no file error with Path = None
    # assert make_ballots.make_ballots(_edf=None) == NO_FILE
    assert validate_edf.validate_edf(test_file) == NO_ERRORS
