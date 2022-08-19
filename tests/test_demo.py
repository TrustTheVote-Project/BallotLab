from electos.ballotmaker.constants import NO_ERRORS
from electos.ballotmaker.demo import demo


def test_demo():
    assert demo() == NO_ERRORS
