"""Ballot data models."""

from dataclasses import dataclass
from typing import List, Union


# --- Type assertions
#
# Python dataclasses don't check field types at runtime, but we want to avoid
# errors.


def _check_type(instance, field, type_):
    """Raise 'TypeError' if 'instance.field' isn't of class 'type'."""
    value = getattr(instance, field)
    if not isinstance(value, type_):
        raise TypeError(
            f"Field '{field}' is not of type '{type_.__name__}': {value}"
        )


def _check_type_hint(instance, field, type_):
    """Raise 'TypeError' if 'instance.field' isn't of type model 'type'."""
    value = getattr(instance, field)
    if not isinstance(value, type_):
        raise TypeError(
            f"Field '{field}' is not of type '{type_._name}': {value}"
        )


def _check_type_list(instance, field, type_):
    """Raise 'TypeError' if 'instance.field' contents aren't of type 'type'."""
    values = getattr(instance, field)
    if not all(isinstance(value, type_) for value in values):
        raise TypeError(
            f"Values in field '{field}' are not all of type '{type_.__name__}': {values}"
        )


# --- Ballot contest data models


@dataclass
class BallotChoiceData:

    """Data for ballot measure selections."""

    id: str
    choice: str


    def __post_init__(self):
        _check_type(self, "id", str)
        _check_type(self, "choice", str)


@dataclass
class BallotMeasureContestData:

    """Data for ballot measure contests."""

    id: str
    type: str
    title: str
    district: str
    text: str
    choices: List[BallotChoiceData]

    def __post_init__(self):
        _check_type(self, "id", str)
        _check_type(self, "type", str)
        _check_type(self, "title", str)
        _check_type(self, "district", str)
        _check_type(self, "text", str)
        _check_type_hint(self, "choices", List)
        self.choices = [BallotChoiceData(**_) for _ in self.choices]


# --- Candidate contest data models


@dataclass
class PartyData:

    """Data for parties candidates are in."""

    name: str
    abbreviation: str

    def __post_init__(self):
        _check_type(self, "name", str)
        _check_type(self, "abbreviation", str)


@dataclass
class CandidateChoiceData:

    """Data for candidate contest selections."""

    id: str
    name: List[str]
    party: List[PartyData]
    is_write_in: bool

    def __post_init__(self):
        _check_type(self, "id", str)
        _check_type_hint(self, "name", List)
        _check_type_list(self, "name", str)
        _check_type_hint(self, "party", List)
        self.party = [PartyData(**_) for _ in self.party]
        _check_type(self, "is_write_in", bool)


@dataclass
class CandidateContestData:

    """Data for candidate contests."""

    id: str
    type: str
    title: str
    district: str
    vote_type: str
    votes_allowed: str
    candidates: List[CandidateChoiceData]

    def __post_init__(self):
        _check_type(self, "id", str)
        _check_type(self, "type", str)
        _check_type(self, "title", str)
        _check_type(self, "district", str)
        _check_type(self, "vote_type", str)
        _check_type(self, "votes_allowed", int)
        _check_type_hint(self, "candidates", List)
        self.candidates = [CandidateChoiceData(**_) for _ in self.candidates]


@dataclass
class BallotStyleData:

    """Date for contests associated with a ballot style."""

    BALLOT_MEASURE = "ballot measure"
    CANDIDATE = "candidate"

    # Note: Don't use separate fields for the types of contests.
    # There's no guarantee the types will be clearly separated in an EDF.
    # (The NIST SP-1500-100 JSON Schema uses unions too.)

    id: str
    scopes: List[str]
    contests: List[Union[BallotMeasureContestData, CandidateContestData]]

    def __post_init__(self):
        _check_type(self, "id", str)
        _check_type_hint(self, "scopes", List)
        _check_type_list(self, "scopes", str)
        _check_type_hint(self, "contests", List)
        contests = []
        for contest in self.contests:
            if not isinstance(contest, dict):
                raise TypeError(f"Contest is not a dictionary: '{contest}'")
            if "type" not in contest:
                raise KeyError(f"Contest has no 'type' field: '{contest}'")
            if contest["type"] not in (self.BALLOT_MEASURE, self.CANDIDATE):
                raise ValueError(f"Unhandled contest type: '{contest['type']}'")
            if contest["type"] == self.BALLOT_MEASURE:
                contest = BallotMeasureContestData(**contest)
            elif contest["type"] == self.CANDIDATE:
                contest = CandidateContestData(**contest)
            contests.append(contest)
        self.contests = contests
