from electos.ballotmaker import make_ballots

from electos.ballotmaker.constants import NO_ERRORS


def test_make_ballots():
    make_ballots_result = make_ballots.make_ballots()
    assert make_ballots_result == NO_ERRORS
