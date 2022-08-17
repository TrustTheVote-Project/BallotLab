from pathlib import Path

from electos.ballotmaker.constants import NO_DATA, NO_ERRORS, NO_FILE
from electos.ballotmaker.election_data import ElectionData

imaginary_file = Path("imaginary_file.json")
test_dir = Path(__file__).parent.resolve()
# this test file must be in the same dir as this test script
test_file = Path("june_test_case.json")
full_test_path = Path(test_dir, test_file)


def test_no_file():
    election_no_file = ElectionData(None)
    assert election_no_file.edf_error == NO_FILE


def test_file_missing():
    election_missing_edf = ElectionData(imaginary_file)
    assert election_missing_edf.edf_error == NO_FILE


def test_read_edf():
    # is the test file available?
    assert full_test_path.is_file()
    election_data = ElectionData(full_test_path)
    assert election_data.edf_error == NO_ERRORS
    # the EDF needs to have at least 1 BallotStyle
    assert election_data.ballot_count > 0
