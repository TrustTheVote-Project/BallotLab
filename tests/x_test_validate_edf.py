from pathlib import Path

from electos.ballotmaker.constants import NO_ERRORS, NO_FILE
from electos.ballotmaker.validate_edf import validate_edf

imaginary_file = Path("imaginary_file.json")
test_dir = Path(__file__).parent.resolve()
# this test JSON files must be in the same dir as this test script
empty_file = Path("empty.json")
empty_file_path = Path(test_dir, empty_file)
test_file = Path("june_test_case.json")
full_test_path = Path(test_dir, test_file)


def test_validate_edf():
    # force a no file error with Path = None
    assert validate_edf(_edf=None) == NO_FILE
    # ensure imaginary_file is actually not a file
    assert not imaginary_file.is_file()
    assert validate_edf(imaginary_file) == NO_FILE

    assert full_test_path.is_file()
    assert validate_edf(full_test_path) == NO_ERRORS
