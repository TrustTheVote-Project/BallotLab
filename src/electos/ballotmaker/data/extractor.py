from typing import Dict, List, Union

from electos.ballotmaker.data.models import ElectionData
from electos.datamodels.nist.indexes import ElementIndex
from electos.datamodels.nist.models.edf import (
    BallotMeasureContest,
    BallotMeasureSelection,
    BallotStyle,
    Candidate,
    CandidateContest,
    CandidateSelection,
    Election,
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


def _text_content(item):
    """Return joined lines from internationalized text."""
    assert isinstance(item, InternationalizedText)
    text = "\n".join(_.content for _ in item.text)
    return text


def _walk_ordered_contests(content: List[OrderedContent]):
    """Walk ordered content yielding contests."""
    for item in content:
        if isinstance(item, OrderedContest):
            yield item
        elif isinstance(item, OrderedHeader):
            yield from _walk_ordered_contests(item.ordered_content)
        else:
            raise TypeError(f"Unexpected type: {type(item).__name__}")


def _walk_ordered_headers(content: List[OrderedContent]):
    """Walk ordered content yielding headers."""
    for item in content:
        if isinstance(item, OrderedHeader):
            yield item
            yield from _walk_ordered_headers(item.ordered_content)
        else:
            raise TypeError(f"Unexpected type: {type(item).__name__}")


# --- Extractor


class BallotDataExtractor:

    """Extract election data from an EDF."""

    def __init__(self):
        pass

    def _ballot_style_external_id(self, ballot_style: BallotStyle):
        """Get the text of a ballot style's external identifier if any."""
        if ballot_style.external_identifier:
            assert (
                len(ballot_style.external_identifier) == 1
            ), "Not ready to handle multiple BallotStyle external IDs"
            name = ballot_style.external_identifier[0].value
        else:
            name = ""
        return name

    def _ballot_style_gp_units(self, ballot_style: BallotStyle):
        """Yield geo-political units for a ballot style."""
        for id_ in ballot_style.gp_unit_ids:
            gp_unit = self._index.by_id(id_)
            yield gp_unit

    def _ballot_style_contests(self, ballot_style: BallotStyle):
        """Yield the contests of a ballot style."""
        for item in _walk_ordered_contests(ballot_style.ordered_content):
            contest = self._index.by_id(item.contest_id)
            yield contest

    def _candidate_name(self, candidate: Candidate):
        """Get the name of a candidate as it appears on a ballot."""
        name = _text_content(candidate.ballot_name)
        return name

    def _candidate_party(self, candidate: Candidate):
        """Get the name and abbreviation of the party of a candidate as it appears on a ballot.

        Drop either field from result if it isn't present.
        """
        # Note: party ID is returned to allow de-duplicating parties in callers.
        id_ = candidate.party_id
        party = self._index.by_id(id_)
        name = _text_content(party.name) if party else None
        abbreviation = (
            _text_content(party.abbreviation)
            if party and party.abbreviation
            else None
        )
        result = {}
        if name:
            result["name"] = name
        if abbreviation:
            result["abbreviation"] = abbreviation
        return result, id_

    def _candidate_contest_candidates(self, contest: CandidateContest):
        """Get candidates for contest, grouped by slate/ticket.

        A slate has:

        - A single ID for the contest selection
        - Collects candidate names into an array.
        - Collects candidate parties into an array.
          - If all candidates in a race share a single party they are combined into
            one entry in the array.
          - If any candidates differ from the others, parties are listed separately.

        Notes:
            - There's no clear guarantee of a 1:1 relationship between slates/tickets
              and parties.
        """
        # Collect individual candidates
        candidates = []
        for selection in contest.contest_selection:
            assert isinstance(
                selection, CandidateSelection
            ), f"Unexpected non-candidate selection: {type(selection).__name__}"
            names = []
            parties = []
            _party_ids = set()
            if selection.candidate_ids:
                for id_ in selection.candidate_ids:
                    candidate = self._index.by_id(id_)
                    name = self._candidate_name(candidate)
                    if name:
                        names.append(name)
                    party, _party_id = self._candidate_party(candidate)
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
                "is_write_in": bool(selection.is_write_in),
            }
            candidates.append(result)
        return candidates

    def _candidate_contest_offices(self, contest: CandidateContest):
        """Get any offices associated with a candidate contest."""
        offices = []
        if contest.office_ids:
            for id_ in contest.office_ids:
                office = self._index.by_id(id_)
                name = _text_content(office.name)
                offices.append(name)
        return offices

    def _candidate_contest_parties(self, contest: CandidateContest):
        """Get any parties associated with a candidate contest."""
        parties = []
        if contest.primary_party_ids:
            for id_ in contest.primary_party_ids:
                party = self._index.by_id(id_)
                name = _text_content(party.name)
                parties.append(name)
        return parties

    def _contest_election_district(self, contest: Contest):
        """Get the district name of a contest."""
        district = self._index.by_id(contest.election_district_id)
        district = _text_content(district.name)
        return district

    def _candidate_contest_of(self, contest: CandidateContest):
        """Extract candidate contest subset needed for a ballot."""
        district = self._contest_election_district(contest)
        offices = self._candidate_contest_offices(contest)
        parties = self._candidate_contest_parties(contest)
        candidates = self._candidate_contest_candidates(contest)
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

    def _ballot_measure_contest_of(self, contest: BallotMeasureContest):
        """Extract ballot measure contest subset needed for a ballot."""
        choices = []
        for selection in contest.contest_selection:
            assert isinstance(
                selection, BallotMeasureSelection
            ), f"Unexpected non-ballot measure selection: {type(selection).__name__}"
            choice = _text_content(selection.selection)
            choices.append(
                {
                    "id": selection.model__id,
                    "choice": choice,
                }
            )
        district = self._contest_election_district(contest)
        full_text = _text_content(contest.full_text)
        result = {
            "id": contest.model__id,
            "type": "ballot measure",
            "title": contest.name,
            "district": district,
            "text": full_text,
            "choices": choices,
        }
        return result

    def _contests(self, ballot_style: BallotStyle):
        """Extract contest subset needed for ballots."""
        for contest in self._ballot_style_contests(ballot_style):
            if isinstance(contest, CandidateContest):
                entry = self._candidate_contest_of(contest)
            elif isinstance(contest, BallotMeasureContest):
                entry = self._ballot_measure_contest_of(contest)
            else:
                # Ignore other contest types
                print(f"Skipping contest of type {contest.model__type}")
            yield entry

    def _election_ballot_styles(self, election: Election):
        """Extract all ballot styles."""
        for ballot_style in election.ballot_style:
            data = {
                "id": self._ballot_style_external_id(ballot_style),
                "scopes": [
                    _text_content(self._index.by_id(_.model__id).name)
                    for _ in self._ballot_style_gp_units(ballot_style)
                ],
                "contests": [_ for _ in self._contests(ballot_style)],
            }
            yield data

    def _elections(self, election_report: ElectionReport):
        """Extract all elections."""
        # In most cases there isn't more than one 'Election' in a report, but the
        # standard allows more than one, so handle them.
        for election in election_report.election:
            data = {
                "name": _text_content(election.name),
                "type": election.type.value,
                "start_date": election.start_date.strftime("%Y-%m-%d"),
                "end_date": election.end_date.strftime("%Y-%m-%d"),
                "ballot_styles": [
                    _ for _ in self._election_ballot_styles(election)
                ],
            }
            yield data

    def extract(self, data: Dict, index: ElementIndex = None) -> ElectionData:
        """Extract election data.

        This is the primary entry point for the extractor.

        Parameters:
            data: An EDF / election report dictionary.
            index: An ElementIndex.
                If empty (the default), create a new index from the election report.
                Use this parameter only if there's already an existing index.

        Returns:
            Election data model for use in ballot rendering.
        """
        election_report = ElectionReport(**data)
        self._index = index or ElementIndex(election_report, "ElectionResults")
        election_data = [
            ElectionData(**_) for _ in self._elections(election_report)
        ]
        return election_data
