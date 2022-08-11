from pathlib import Path

from electos.ballotmaker import validate_edf
from electos.ballotmaker.constants import NO_DATA, NO_ERRORS, NO_FILE

not_a_file = Path("not_a_file.json")
test_dir = Path(__file__).parent.resolve()
# this test JSON files must be in the same dir as this test script
empty_file = Path("empty.json")
empty_file_path = Path(test_dir, empty_file)
test_file = Path("june_test_case.json")
full_test_path = Path(test_dir, test_file)


def test_validate_edf():
    # force a no file error with Path = None
    # assert make_ballots.make_ballots(_edf=None) == NO_FILE
    assert validate_edf.validate_edf(_edf=None) == NO_FILE
    # ensure not_a_file is actually not a file
    assert Path.is_file(not_a_file) == False
    assert validate_edf.validate_edf(not_a_file) == NO_FILE
    # test empty json file
    # assert Path.is_file(empty_file_path)
    # assert validate_edf.validate_edf(empty_file_path) == NO_DATA

    assert Path.is_file(full_test_path)
    assert validate_edf.validate_edf(full_test_path) == NO_ERRORS
