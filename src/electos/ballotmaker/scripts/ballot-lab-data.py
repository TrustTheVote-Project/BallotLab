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
    candidates = []
    write_ins = 0
    for selection in contest.contest_selection:
        assert isinstance(selection, CandidateSelection), \
            f"Unexpected non-candidate selection: {type(selection).__name__}"
        # Write-ins have no candidate IDs
        if selection.candidate_ids:
            for id_ in selection.candidate_ids:
                candidate = index.by_id(id_)
                candidates.append(candidate)
        if selection.is_write_in:
            write_ins += 1
    result = {
        "title": contest.name,
        "type": "candidate",
        "vote_type": contest.vote_variation.value,
        "district": district,
        "candidates": [candidate_name(_) for _ in candidates],
        "write_ins": write_ins,
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
