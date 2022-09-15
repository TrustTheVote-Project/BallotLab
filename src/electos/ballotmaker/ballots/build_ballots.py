from datetime import datetime
from pathlib import Path

from electos.ballotmaker.data.models import ElectionData


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
    
def build_ballots(election: ElectionData):


    now = datetime.now()
    date_time = now.strftime("%Y_%m_%dT%H%M%S")
    home_dir = Path.home()

    for ballot_data in election.ballot_styles:
        pass
