import logging

from electos.ballotmaker.constants import NO_ERRORS
from electos.ballotmaker.demo_election_data import DemoElectionData

log = logging.getLogger(__name__)


def demo():
    log.debug("Starting ballotlab demo ...")
    demo_data = DemoElectionData()
    return NO_ERRORS
