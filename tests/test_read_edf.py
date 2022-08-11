from pathlib import Path

from electos.ballotmaker.read_edf import read_edf

test_dir = Path(__file__).parent.resolve()
# this test file must be in the same dir as this test script
test_file = Path("june_test_case.json")
full_test_path = Path(test_dir, test_file)


def test_read_edf():
    # is the test file available?
    assert full_test_path.is_file()
    # the EDF needs to have at least 1 BallotStyle
    assert read_edf(full_test_path) >= 1
