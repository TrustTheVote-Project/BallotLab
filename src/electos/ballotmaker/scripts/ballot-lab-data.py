from typing import List, Union

from electos.datamodels.nist.models.edf import *
from electos.datamodels.nist.indexes import ElementIndex

OrderedContent = Union[OrderedContest, OrderedHeader]


# --- Utilities


def text_content(item):
    """Return joined lines in internationalized text."""
    assert isinstance(item, InternationalizedText)
    text = "\n".join(_.content for _ in item.text)
    return text


def walk_ordered_content(content: List[OrderedContent]):
    for item in content:
        if isinstance(item, OrderedContest):
            yield item
        elif isinstance(item, OrderedHeader):
            yield item
            yield from walk_ordered_content(item.ordered_content)
        else:
            raise TypeError(f"Unexpected type: {type(item).__name__}")


# --- Ballot Properties


def all_ballot_styles(election_report: ElectionReport, index):
    for ballot_style in index.by_type("BallotStyle"):
        yield ballot_style


def ballot_style_name(ballot_style: BallotStyle):
    assert len (ballot_style.external_identifier) == 1, \
        "Not ready to handle multiple BallotStyle external IDs"
    name = ballot_style.external_identifier[0].value
    return name


def ballot_style_gp_units(ballot_style: BallotStyle, index):
    for id_ in ballot_style.gp_unit_ids:
        gp_unit = index.by_id(id_)
        yield gp_unit


def ballot_style_contests(ballot_style: BallotStyle, index):
    for item in walk_ordered_content(ballot_style.ordered_content):
        contest = index.by_id(item.contest_id)
        yield contest


def ballot_style_candidate_contests(ballot_style: BallotStyle, index):
    for contest in ballot_style_contests(ballot_style, index):
        if not isinstance(contest, CandidateContest):
            continue
        candidates = []
        for selection in contest.contest_selection:
            assert isinstance(selection, CandidateSelection), \
                "Unexpected non-candidate selection: {type(selection).__name__}"
            # Ignore write-ins for tier 1
            if selection.is_write_in:
                continue
            for id_ in selection.candidate_ids:
                candidate = index.by_id(id_)
                candidates.append(candidate)
        yield contest, candidates


def candidate_name(candidate: Candidate):
    name = text_content(candidate.ballot_name)
    return name


# --- Main

import json
import sys
from pathlib import Path


def report(root, index):
    ballot_styles = list(all_ballot_styles(root, index))
    # Only look at the first index
    ballot_style = ballot_styles[0]
    name = ballot_style_name(ballot_style)
    print("name:", name)
    gp_units = ballot_style_gp_units(ballot_style, index)
    print("gp units:")
    for item in gp_units:
        print(f"- {text_content(item.name)}")
    print("contests:")
    contests = ballot_style_candidate_contests(ballot_style, index)
    for contest, candidates in contests:
        print(f"- name: {contest.name}")
        print(f"  type: {contest.vote_variation.value}")
        print(f"  votes: {contest.votes_allowed}")
        print(f"  candidates:")
        for candidate in candidates:
            print(f"  - {candidate_name(candidate)}")


def main():
    file = Path(sys.argv[1])
    with file.open() as input:
        text = input.read()
        data = json.loads(text)
    edf = ElectionReport(**data)
    index = ElementIndex(edf, "ElectionResults")
    report(edf, index)


if __name__ == '__main__':
    main()
