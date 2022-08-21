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
    for ballot_style in index.by_type("BallotStyle"):
        yield ballot_style


def ballot_style_name(ballot_style: BallotStyle):
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
    for item in walk_ordered_contests(ballot_style.ordered_content):
        contest = index.by_id(item.contest_id)
        yield contest


def ballot_style_candidate_contests(
    ballot_style: BallotStyle, index, keep_write_ins, keep_n_of_m, **opts
):
    for contest in ballot_style_contests(ballot_style, index):
        if not isinstance(contest, CandidateContest):
            continue
        # Ignore N-of-M by default
        if not keep_n_of_m and contest.vote_variation == VoteVariation.N_OF_M:
            continue
        candidates = []
        for selection in contest.contest_selection:
            assert isinstance(selection, CandidateSelection), \
                "Unexpected non-candidate selection: {type(selection).__name__}"
            # Ignore write-ins by default
            if not keep_write_ins and selection.is_write_in:
                continue
            for id_ in selection.candidate_ids:
                candidate = index.by_id(id_)
                candidates.append(candidate)
        yield contest, candidates


def candidate_name(candidate: Candidate):
    name = text_content(candidate.ballot_name)
    return name


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
    nth -= 1
    ballot_style = ballot_styles[nth]
    name = ballot_style_name(ballot_style)
    print("name:", name)
    gp_units = ballot_style_gp_units(ballot_style, index)
    print("gp units:")
    for item in gp_units:
        print(f"- {text_content(item.name)}")
    print("contests:")
    contests = ballot_style_candidate_contests(ballot_style, index, **opts)
    for contest, candidates in contests:
        print(f"- name: {contest.name}")
        print(f"  vote type: {contest.vote_variation.value}")
        print(f"  votes allowed: {contest.votes_allowed}")
        print(f"  candidates:")
        for candidate in candidates:
            print(f"  - {candidate_name(candidate)}")


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
        "--keep-write-ins", action = "store_true",
        help = "Process write in candidates",
    )
    parser.add_argument(
        "--keep-n-of-m", action = "store_true",
        help = "Process N-of-M contests",
    )
    opts = parser.parse_args()
    file = opts.file
    opts = vars(opts)

    with file.open() as input:
        text = input.read()
        data = json.loads(text)
    edf = ElectionReport(**data)
    index = ElementIndex(edf, "ElectionResults")
    report(edf, index, **opts)


if __name__ == '__main__':
    main()
