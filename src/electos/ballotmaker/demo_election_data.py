import logging
from dataclasses import dataclass, field

log = logging.getLogger(__name__)


def get_election_header() -> dict:
    return {
        "Name": "General Election",
        "StartDate": "2024-11-05",
        "EndDate": "2024-11-05",
        "Type": "general",
        "ElectionScope": "United States of America",
    }


@dataclass
class DemoElectionData:
    election_header: dict = field(init=False)

    def __post_init__(self):
        self.election_header = get_election_header()
        log.debug(f"Election Name: {self.election_header.get('Name')}")
