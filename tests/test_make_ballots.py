from pathlib import Path

from electos.ballotmaker import make_ballots
from electos.ballotmaker.constants import NO_ERRORS, NO_FILE

test_file = Path("empty.json")


def test_make_ballots():
    # force a no file error with Path = None
    assert make_ballots.make_ballots(_edf=None) == NO_FILE
    assert make_ballots.make_ballots(test_file) == NO_ERRORS
