import json
import logging

from electos.ballotmaker.ballots.build_ballots import build_ballots
from electos.ballotmaker.ballots.files import FileTools
from electos.ballotmaker.data.extractor import BallotDataExtractor
from electos.ballotmaker.data.models import ElectionData


def main():
    # set up logging for ballot creation
    # format output and point to log
    logging.getLogger(__name__)
    logging.basicConfig(
        stream=None,
        level=logging.INFO,
        format="{asctime} - {message}",
        style="{",
    )

    # get the EDF file from the assets directory,
    # a "known-good" source of election data
    data_file_name = "september_test_case.json"
    relative_path = "assets/data"
    data_file = FileTools(data_file_name, relative_path)
    full_data_path = data_file.abs_path_to_file

    return build_ballots(get_election_data(full_data_path))


def get_election_data(edf_file: str) -> ElectionData:
    logging.info(f"Using EDF {edf_file}")
    with edf_file.open() as input:
        text = input.read()
        data = json.loads(text)

    extractor = BallotDataExtractor()
    election_report = extractor.extract(data)
    # because we're hard-coding the EDF file, we know it only
    # contains data for one election!
    election_data = election_report[0]
    # assert isinstance(election_data, ElectionData)
    logging.info(f"Found ballots for {election_data.name}")
    return election_data


if __name__ == "__main__":  # pragma: no cover
    main()
