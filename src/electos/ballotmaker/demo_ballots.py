import json
import logging

from electos.ballotmaker.ballots.files import FileTools
from electos.ballotmaker.data.extractor import BallotDataExtractor
from electos.ballotmaker.data.models import ElectionData

log = logging.getLogger(__name__)

data_file_name = "september_test_case.json"
relative_path = "assets/data"
data_file = FileTools(data_file_name, relative_path)
full_data_path = data_file.abs_path_to_file


def get_election_data():
    with full_data_path.open() as input:
        text = input.read()
        data = json.loads(text)

    extractor = BallotDataExtractor()
    election_data = extractor.extract(data)
    # assert isinstance(election_data, ElectionData)
    print(election_data.ElectionData.name)


if __name__ == "__main__":  # pragma: no cover
    get_election_data()
