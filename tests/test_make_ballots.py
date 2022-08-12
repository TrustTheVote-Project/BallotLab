from pathlib import Path

from electos.ballotmaker.constants import NO_ERRORS, NO_FILE
from electos.ballotmaker.make_ballots import make_ballots

imaginary_file = Path("imaginary_file.json")
test_dir = Path(__file__).parent.resolve()
test_file = Path("june_test_case.json")
full_test_path = Path(test_dir, test_file)


def test_make_ballots():
    # force a no file error with Path = None
    assert make_ballots(_edf=None) == NO_FILE
    # ensure imaginary_file is actually not a file
    assert not imaginary_file.is_file()
    assert make_ballots(imaginary_file) == NO_FILE
    assert full_test_path.is_file()
    assert make_ballots(full_test_path) == NO_ERRORS
