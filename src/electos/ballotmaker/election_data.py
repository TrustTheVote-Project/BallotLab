import json
import logging
from dataclasses import dataclass, field
from pathlib import Path

from electos.ballotmaker.constants import NO_DATA, NO_ERRORS, NO_FILE
from electos.datamodels.nist.indexes.element_index import ElementIndex
from electos.datamodels.nist.models.edf import ElectionReport

log = logging.getLogger(__name__)


@dataclass
class ElectionData:
    edf: Path
    # properties retrieved from the EDF
    edf_error: int = field(init=False)
    election_report: ElectionReport = field(init=False)
    ballot_styles: ElementIndex = field(init=False)
    ballot_count: int = field(init=False)
    election_name: str = field(init=False)
    start_date: str = field(init=False)
    end_date: str = field(init=False)
    election_type: str = field(init=False)

    def __post_init__(self):
        # let's assume there are no errors
        self.edf_error = NO_ERRORS
        # haven't found any ballots yet
        self.ballot_count = 0

        # ensure the EDF is a valid file
        if self.edf is None:
            log.debug("No EDF file provided.")
            self.edf_error = NO_FILE
            return
        if not self.edf.is_file():
            log.debug(f"EDF {self.edf} is not a file")
            self.edf_error = NO_FILE
            return

        # Open the specified EDF file
        edf_data = json.loads(self.edf.read_text())
        self.election_report = ElectionReport(**edf_data)

        # get election header data
        self.election_name = (
            self.election_report.election[0].name.text[0].content
        )
        log.info(f"Election: {self.election_name}")

        self.start_date = self.election_report.election[0].start_date
        log.info(f"Start date: {self.start_date}")
        self.end_date = self.election_report.election[0].end_date
        log.info(f"End date: {self.end_date}")
        self.election_type = self.election_report.election[0].type
        log.info(f"{self.election_type}")

        # index the election report to retrieve lists
        index = ElementIndex(self.election_report, "ElectionResults")

        # how many ballots?
        self.ballot_styles = index.by_type("ElectionResults.BallotStyle")
        # list and count ballots
        for count, ballot in enumerate(self.ballot_styles, start=1):
            ballot_value = ballot.external_identifier[0].value
            log.info(f"Ballot: {ballot_value}")
        self.ballot_count = count
        log.info(f"Found {self.ballot_count} ballot styles in {self.edf}")
