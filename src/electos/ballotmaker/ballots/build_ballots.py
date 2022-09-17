import logging
from datetime import datetime
from pathlib import Path

from electos.ballotmaker.ballots.ballot_layout import build_ballot
from electos.ballotmaker.constants import PROGRAM_NAME
from electos.ballotmaker.data.models import ElectionData

logging.getLogger(__name__)


def get_election_header(election: ElectionData) -> dict:
    """extract the shared data for ballot headers"""
    name = election.name
    end_date = election.end_date
    election_type = election.type
    return {
        "Name": name,
        "EndDate": end_date,
        "Type": election_type,
    }


def build_ballots(election: ElectionData) -> Path:

    # create the directories needed
    now = datetime.now()
    date_time = now.strftime("%Y_%m_%dT%H%M%S")
    home_dir = Path.home()
    program_dir = Path(home_dir, PROGRAM_NAME)
    new_ballot_dir = Path(program_dir, date_time)
    logging.info(f"New ballots will be saved in {new_ballot_dir}")
    Path(new_ballot_dir).mkdir(parents=True, exist_ok=False)
    logging.info("Output directory created.")
    election_header = get_election_header(election)

    for ballot_data in election.ballot_styles:
        logging.info(f"Generating ballot for {ballot_data.id}")
        new_ballot_name = build_ballot(
            ballot_data, election_header, new_ballot_dir
        )
    return new_ballot_dir
