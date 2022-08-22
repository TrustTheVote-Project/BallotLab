import logging

from electos.ballotmaker.ballots.demo_ballot import build_ballot
from electos.ballotmaker.constants import NO_ERRORS

log = logging.getLogger(__name__)


def make_demo_ballot():
    log.debug("Starting ballotlab demo ...")
    build_ballot()
    return NO_ERRORS
