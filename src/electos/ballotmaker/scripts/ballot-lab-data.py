from itertools import groupby
from typing import List, Union

from electos.datamodels.nist.models.edf import *
from electos.datamodels.nist.indexes import ElementIndex


# --- Base Types
#
# Schema expresses these as union types not subclasses

Contest = Union[BallotMeasureContest, CandidateContest]

OrderedContent = Union[OrderedContest, OrderedHeader]


# --- Utilities


def text_content(item):
    """Return joined lines from internationalized text."""
    assert isinstance(item, InternationalizedText)
    text = "\n".join(_.content for _ in item.text)
    return text


def walk_ordered_contests(content: List[OrderedContent]):
    """Walk ordered content yielding contests."""
    for item in content:
        if isinstance(item, OrderedContest):
            yield item
        elif isinstance(item, OrderedHeader):
            yield from walk_ordered_contests(item.ordered_content)
        else:
            raise TypeError(f"Unexpected type: {type(item).__name__}")


def walk_ordered_headers(content: List[OrderedContent]):
    """Walk ordered content yielding headers."""
    for item in content:
        if isinstance(item, OrderedHeader):
            yield item
            yield from walk_ordered_headers(item.ordered_content)
        else:
            raise TypeError(f"Unexpected type: {type(item).__name__}")


# --- Ballot Properties


def all_ballot_styles(election_report: ElectionReport, index):
    """Yield all ballot styles."""
    for ballot_style in index.by_type("BallotStyle"):
        yield ballot_style


def ballot_style_id(ballot_style: BallotStyle):
    """Get the text of a ballot style's external identifier if any."""
    if ballot_style.external_identifier:
        assert len(ballot_style.external_identifier) == 1, \
            "Not ready to handle multiple BallotStyle external IDs"
        name = ballot_style.external_identifier[0].value
    else:
        name = ""
    return name


def ballot_style_gp_units(ballot_style: BallotStyle, index):
    for id_ in ballot_style.gp_unit_ids:
        gp_unit = index.by_id(id_)
        yield gp_unit


def ballot_style_contests(ballot_style: BallotStyle, index):
    """Yield the contests of a ballot style."""
    for item in walk_ordered_contests(ballot_style.ordered_content):
        contest = index.by_id(item.contest_id)
        yield contest


def candidate_name(candidate: Candidate):
    """Get the name of a candidate as it appears on a ballot."""
    name = text_content(candidate.ballot_name)
    return name


def candidate_party(candidate: Candidate, index):
    """Get the name and abbreviation of the party of a candidate as it appears on a ballot."""
    # Note: party ID is returned to allow de-duplicating parties in callers.
    id_ = candidate.party_id
    party = index.by_id(id_)
    name = text_content(party.name) if party else ""
    abbreviation = text_content(party.abbreviation) if party and party.abbreviation else ""
    result = {
        "name": name,
        "abbreviation": abbreviation,
    }
    return result, id_


def candidate_contest_candidates(contest: CandidateContest, index):
    """Get candidates for contest, grouped by slate/ticket.

    A slate has:

    - A single ID for the contest selection
    - Collects candidate names into an array.
    - Collects candidate parties into an array.
      - If all candidates in a race share a single party they are combined into
        one entry in the array.
      - If any candidates differ from the others, parties are listed separately.

    Notes:
        - There's no clear guarantee of a 1:1 relationship between slates and parties.
    """
    # Collect individual candidates
    candidates = []
    for selection in contest.contest_selection:
        assert isinstance(selection, CandidateSelection), \
            f"Unexpected non-candidate selection: {type(selection).__name__}"
        names = []
        parties = []
        _party_ids = set()
        if selection.candidate_ids:
            for id_ in selection.candidate_ids:
                candidate = index.by_id(id_)
                name = candidate_name(candidate)
                if name:
                    names.append(name)
                party, _party_id = candidate_party(candidate, index)
                parties.append(party)
                _party_ids.add(_party_id)
        # If there's only one party ID, all candidates share the same party.
        # If there's any divergence track them all individually.
        if len(_party_ids) == 1:
            parties = parties[:1]
        result = {
            "id": selection.model__id,
            "name": names,
            "party": parties,
            "is_write_in": bool(selection.is_write_in)
        }
        candidates.append(result)
    return candidates


def candidate_contest_offices(contest: CandidateContest, index):
    """Get any offices associated with a candidate contest."""
    offices = []
    if contest.office_ids:
        for id_ in contest.office_ids:
            office = index.by_id(id_)
            name = text_content(office.name)
            offices.append(name)
    return offices


def candidate_contest_parties(contest: CandidateContest, index):
    """Get any parties associated with a candidate contest."""
    parties = []
    if contest.primary_party_ids:
        for id_ in contest.primary_party_ids:
            party = index.by_id(id_)
            name = text_content(party.name)
            parties.append(name)
    return parties


def contest_election_district(contest: Contest, index):
    """Get the district name of a contest."""
    district = index.by_id(contest.election_district_id)
    district = text_content(district.name)
    return district


# Gather & Extract
#
# Results are data needed for ballot generation.

def extract_candidate_contest(contest: CandidateContest, index):
    """Extract candidate contest information needed for ballots."""
    district = contest_election_district(contest, index)
    offices = candidate_contest_offices(contest, index)
    parties = candidate_contest_parties(contest, index)
    candidates = candidate_contest_candidates(contest, index)
    result = {
        "id": contest.model__id,
        "title": contest.name,
        "type": "candidate",
        "vote_type": contest.vote_variation.value,
        # Include even when default is 1: don't require caller to track that.
        "votes_allowed": contest.votes_allowed,
        "district": district,
        "candidates": candidates,
        # "offices": offices,
        # "parties": parties,
    }
    return result


def extract_ballot_measure_contest(contest: BallotMeasureContest, index):
    """Extract ballot measure contest information needed for ballots."""
    choices = []
    for selection in contest.contest_selection:
        assert isinstance(selection, BallotMeasureSelection), \
           f"Unexpected non-ballot measure selection: {type(selection).__name__}"
        choice = text_content(selection.selection)
        choices.append(choice)
    district = contest_election_district(contest, index)
    full_text = text_content(contest.full_text)
    result = {
        "title": contest.name,
        "type": "ballot measure",
        "district": district,
        "choices": choices,
        "text": full_text,
    }
    return result


def gather_contests(ballot_style: BallotStyle, index):
    """Extract all contest information needed for ballots."""
    contests = {
        kind: [] for kind in ("candidate", "ballot_measure")
    }
    for contest in ballot_style_contests(ballot_style, index):
        if isinstance(contest, CandidateContest):
            entry = extract_candidate_contest(contest, index)
            contests["candidate"].append(entry)
        elif isinstance(contest, BallotMeasureContest):
            entry = extract_ballot_measure_contest(contest, index)
            contests["ballot_measure"].append(entry)
        else:
            # Ignore other contest types
            print(f"Skipping contest of type {contest.model__type}")
    return contests


# --- Main

import argparse
import json
from pathlib import Path


def report(root, index, nth, **opts):
    """Generate data needed by BallotLab"""
    ballot_styles = list(all_ballot_styles(root, index))
    if not (1 <= nth <= len(ballot_styles)):
        print(f"Ballot styles: {nth} is out of range [1-{len(ballot_styles)}]")
        return
    ballot_style = ballot_styles[nth - 1]
    data = {}
    id_ = ballot_style_id(ballot_style)
    data["ballot_style"] = id_
    contests = gather_contests(ballot_style, index)
    if not contests:
        print(f"No contests found for ballot style: {id_}\n")
    data["contests"] = contests
    print(json.dumps(data, indent = 4))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file", type = Path,
        help = "Test case data (JSON)"
    )
    parser.add_argument(
        "nth", nargs = "?", type = int, default = 1,
        help = "Index of the ballot style, starting from 1 (default: 1)"
    )
    parser.add_argument(
        "--debug", action = "store_true",
        help = "Enable debugging output and stack traces"
    )
    opts = parser.parse_args()
    file = opts.file
    opts = vars(opts)

    try:
        with file.open() as input:
            text = input.read()
            data = json.loads(text)
        edf = ElectionReport(**data)
        index = ElementIndex(edf, "ElectionResults")
        report(edf, index, **opts)
    except Exception as ex:
        if opts["debug"]:
            raise ex
        print("error:", ex)


if __name__ == '__main__':
    main()
