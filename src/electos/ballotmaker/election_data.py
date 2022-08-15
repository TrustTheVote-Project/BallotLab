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
    edf_error: int = field(init=False)
    election_report: ElectionReport = field(init=False)
    ballot_styles: ElementIndex = field(init=False)
    ballot_count: int = field(init=False)
    election_name: str = field(init=False)

    def __post_init__(self):
        # let's assume there are no errors
        self.edf_error = NO_ERRORS
        # haven't found any ballots yet
        self.ballot_count = 0

        if self.edf is None:
            log.debug("No EDF file provided.")
            self.edf_error = NO_FILE
            return
        if not self.edf.is_file():
            log.debug(f"EDF {self.edf} is not a file")
            self.edf_error = NO_FILE
            return

        """Opens the specified EDF file, counts the number of BallotStyles"""
        edf_data = json.loads(self.edf.read_text())
        self.election_report = ElectionReport(**edf_data)
        # get election header data
        self.election_name = (
            self.election_report.election[0].name.text[0].content
        )
        log.info(f"Election: {self.election_name}")
        index = ElementIndex(self.election_report, "ElectionResults")
        self.ballot_styles = index.by_type("ElectionResults.BallotStyle")
        # self.ballot_count = sum(1 for _ in self.ballot_styles)
        for count, ballot in enumerate(self.ballot_styles, start=1):
            ballot_value = ballot.external_identifier[0].value
            log.info(f"Ballot: {ballot_value}")
        self.ballot_count = count
        log.info(f"Found {self.ballot_count} ballot styles in {self.edf}")
        # self.election_header = index.by_type("ElectionResults.Election")
        # for element in self.election_header:
        #     log.info(f"Element: {element}")
        # log.info(f"Header: {self.election_header}")
        # loop through all types in index
        # for model_type in index.types():
        #     log.info(f"Model type: {model_type}")
        #     for element in index.by_type(model_type):
        #         log.info(f"Element: {element}")
        #         # Do something with 'elements'
