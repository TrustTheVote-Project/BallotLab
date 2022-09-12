from typing import List, Union

from electos.datamodels.nist.indexes import ElementIndex
from electos.datamodels.nist.models.edf import (
    BallotMeasureContest,
    BallotMeasureSelection,
    BallotStyle,
    Candidate,
    CandidateContest,
    CandidateSelection,
    ElectionReport,
    InternationalizedText,
    OrderedContest,
    OrderedHeader,
)


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


def ballot_style_external_id(ballot_style: BallotStyle):
    """Get the text of a ballot style's external identifier if any."""
    if ballot_style.external_identifier:
        assert len(ballot_style.external_identifier) == 1, \
            "Not ready to handle multiple BallotStyle external IDs"
        name = ballot_style.external_identifier[0].value
    else:
        name = ""
    return name


def ballot_style_gp_units(ballot_style: BallotStyle, index):
    """Yield geo-political units for a ballot style."""
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
    """Get the name and abbreviation of the party of a candidate as it appears on a ballot.

    Drop either field from result if it isn't present.
    """
    # Note: party ID is returned to allow de-duplicating parties in callers.
    id_ = candidate.party_id
    party = index.by_id(id_)
    name = text_content(party.name) if party else None
    abbreviation = text_content(party.abbreviation) if party and party.abbreviation else None
    result = {}
    if name:
        result["name"] = name
    if abbreviation:
        result["abbreviation"] = abbreviation
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
                if party:
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


# --- Extraction
#
# Gather and select data needed for ballot generation.

def extract_candidate_contest(contest: CandidateContest, index):
    """Extract candidate contest subset needed for a ballot."""
    district = contest_election_district(contest, index)
    offices = candidate_contest_offices(contest, index)
    parties = candidate_contest_parties(contest, index)
    candidates = candidate_contest_candidates(contest, index)
    result = {
        "id": contest.model__id,
        "type": "candidate",
        "title": contest.name,
        "district": district,
        "vote_type": contest.vote_variation.value,
        # Include even when default is 1: don't require caller to track that.
        "votes_allowed": contest.votes_allowed,
        "candidates": candidates,
        # "offices": offices,
        # "parties": parties,
    }
    return result


def extract_ballot_measure_contest(contest: BallotMeasureContest, index):
    """Extract ballot measure contest subset needed for a ballot."""
    choices = []
    for selection in contest.contest_selection:
        assert isinstance(selection, BallotMeasureSelection), \
           f"Unexpected non-ballot measure selection: {type(selection).__name__}"
        choice = text_content(selection.selection)
        choices.append({
            "id": selection.model__id,
            "choice": choice,
        })
    district = contest_election_district(contest, index)
    full_text = text_content(contest.full_text)
    result = {
        "id": contest.model__id,
        "type": "ballot measure",
        "title": contest.name,
        "district": district,
        "text": full_text,
        "choices": choices,
    }
    return result


def extract_contests(ballot_style: BallotStyle, index):
    """Extract contest subset needed for ballots."""
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


def extract_ballot_styles(election_report: ElectionReport, index):
    """Extract all ballot styles."""
    for ballot_style in index.by_type("BallotStyle"):
        yield ballot_style
