from pathlib import Path

from electos.ballotmaker import make_ballots
from electos.ballotmaker.constants import NO_ERRORS, NO_FILE

not_a_file = Path("not_a_file.json")
test_dir = Path(__file__).parent.resolve()
test_file = Path("june_test_case.json")
full_test_path = Path(test_dir, test_file)


def test_make_ballots():
    # force a no file error with Path = None
    assert make_ballots.make_ballots(_edf=None) == NO_FILE
    # ensure not_a_file is actually not a file
    assert Path.is_file(not_a_file) == False
    assert make_ballots.make_ballots(not_a_file) == NO_FILE
    assert Path.is_file(full_test_path)
    assert make_ballots.make_ballots(full_test_path) == NO_ERRORS
