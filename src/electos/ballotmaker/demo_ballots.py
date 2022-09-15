import json
import logging

from electos.ballotmaker.ballots.files import FileTools
from electos.ballotmaker.data.extractor import BallotDataExtractor
from electos.ballotmaker.data.models import ElectionData

log = logging.getLogger(__name__)

# get the EDF file from the assets directory,
# a "known-good" source of election data
data_file_name = "september_test_case.json"
relative_path = "assets/data"
data_file = FileTools(data_file_name, relative_path)
full_data_path = data_file.abs_path_to_file


def get_election_data() -> ElectionData:
    with full_data_path.open() as input:
        text = input.read()
        data = json.loads(text)

    extractor = BallotDataExtractor()
    election_report = extractor.extract(data)
    # because we're hard-coding the EDF file, we know it only
    # contains data for one election!
    election_data = election_report[0]
    # assert isinstance(election_data, ElectionData)
    log.info(f"Generating demo ballots for {election_data.name}")
    return election_data


def make_election_ballots(election: ElectionData):

    pass


if __name__ == "__main__":  # pragma: no cover
    get_election_data()
