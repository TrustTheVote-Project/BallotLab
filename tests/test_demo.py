from electos.ballotmaker.constants import NO_ERRORS
from electos.ballotmaker.demo import make_demo_ballot


def test_demo():
    assert make_demo_ballot() == NO_ERRORS
