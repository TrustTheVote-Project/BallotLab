from pathlib import Path

from electos.ballotmaker import read_edf
from genericpath import isfile

test_dir = Path(__file__).parent.resolve()
# this test file must be in the same dir as this test script
test_file = Path("june_test_case.json")
full_test_path = Path(test_dir, test_file)


def test_read_edf():
    # is the test file available?
    assert isfile(full_test_path)
    # the EDF needs to have at least 1 BallotStyle
    assert read_edf.read_edf(full_test_path) >= 1
