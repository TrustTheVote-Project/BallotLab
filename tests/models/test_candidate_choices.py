import pytest

from pytest import raises
from contextlib import nullcontext as raises_none

from dataclasses import asdict

from electos.ballotmaker.data.models import (
    CandidateChoiceData,
    PartyData,
)


# Tests

CANDIDATE_CHOICE_TESTS = [
    # Single candidate, no party
    (
        {
            "id": "candidate-contest-1--candidate-1",
            "name": [
                "Anthony Alpha",
            ],
            "party": [],
            "is_write_in": False,
        },
        raises_none(),
    ),
    # Multiple candidates, no party
    (
        {
            "id": "candidate-contest-1--candidate-1",
            "name": [
                "Anthony Alpha",
                "Betty Beta",
            ],
            "party": [],
            "is_write_in": False,
        },
        raises_none(),
    ),
    # Multiple candidates, single party
    (
        {
            "id": "candidate-contest-1--candidate-1",
            "name": [
                "Anthony Alpha",
                "Betty Beta",
            ],
            "party": [
                {
                    "name": "Lepton Party",
                    "abbreviation": "LEP",
                },
            ],
            "is_write_in": False,
        },
        raises_none(),
    ),
    # Multiple candidates, same number of parties
    (
        {
            "id": "candidate-contest-1--candidate-1",
            "name": [
                "Anthony Alpha",
                "Elizabeth Epsilon",
            ],
            "party": [
                {
                    "name": "Lepton Party",
                    "abbreviation": "LEP",
                },
                {
                    "name": "Fermion Party",
                    "abbreviation": "FRM",
                },
            ],
            "is_write_in": False,
        },
        raises_none(),
    ),
    # Multiple candidates, differing number of parties
    # Note: should have the same number of parties iff no. of candidates > 1
    pytest.param(
        {
            "id": "candidate-contest-1--candidate-1",
            "name": [
                "Anthony Alpha",
                "Elizabeth Epsilon",
            ],
            "party": [
                {
                    "name": "Lepton Party",
                    "abbreviation": "LEP",
                },
                {
                    "name": "Hadron Party",
                    "abbreviation": "HAD",
                },
                {
                    "name": "Fermion Party",
                    "abbreviation": "FRM",
                },
            ],
            "is_write_in": False,
        },
        raises(ValueError, match = "Counts of names and parties don't match"),
        marks = pytest.mark.xfail(reason = "Mismatched counts of candidate names and parties"),
    ),
    # 'name' shouldn't be empty if 'is_write_in' is False
    pytest.param(
        {
            "id": "candidate-contest-1--candidate-1",
            "name": [],
            "party": [],
            "is_write_in": False,
        },
        raises(ValueError, match = "Candidate name is empty"),
        marks = pytest.mark.xfail(reason = "Empty 'name' list"),
    ),
    # 'name' is empty if 'is_write_in' is True
    (
        {
            "id": "candidate-contest-1--candidate-1",
            "name": [],
            "party": [],
            "is_write_in": True,
        },
        raises_none(),
    ),
    # 'name' must be empty if 'is_write_in' is True
    pytest.param(
        {
            "id": "candidate-contest-1--candidate-1",
            "name": [
                "Anthony Alpha",
            ],
            "party": [],
            "is_write_in": True,
        },
        raises(ValueError, match = "Write-in cannot have a 'name'"),
        marks = pytest.mark.xfail(reason = "Write-ins can't have candidate names"),
    ),
    # 'party' must be empty if 'is_write_in' is True
    pytest.param(
        {
            "id": "candidate-contest-1--candidate-1",
            "name": [],
            "party": [
                {
                    "name": "Lepton Party",
                    "abbreviation": "LEP",
                },
            ],
            "is_write_in": True,
        },
        raises(ValueError, match = "Write-in cannot have a 'party'"),
        marks = pytest.mark.xfail(reason = "Write-ins can't have candidate parties"),
    ),
    # Missing ID
    (
        {
            "name": [
                "Anthony Alpha",
            ],
            "party": [
                {
                    "name": "Lepton Party",
                    "abbreviation": "LEP",
                },
            ],
            "is_write_in": False,
        },
        raises(TypeError, match = "required positional argument: 'id'"),
    ),
    # Missing name
    (
        {
            "id": "candidate-contest-1--candidate-1",
            "party": [
                {
                    "name": "Lepton Party",
                    "abbreviation": "LEP",
                },
            ],
            "is_write_in": False,
        },
        raises(TypeError, match = "required positional argument: 'name'"),
    ),
    # Missing party
    (
        {
            "id": "candidate-contest-1--candidate-1",
            "name": [
                "Anthony Alpha",
            ],
            "is_write_in": False,
        },
        raises(TypeError, match = "required positional argument: 'party'"),
    ),
    # Missing 'is write-in'
    (
        {
            "id": "candidate-contest-1--candidate-1",
            "name": [
                "Anthony Alpha",
            ],
            "party": [
                {
                    "name": "Lepton Party",
                    "abbreviation": "LEP",
                },
            ],
        },
        raises(TypeError, match = "required positional argument: 'is_write_in'"),
    ),
    # Empty object
    (
        {},
        raises(TypeError, match = "required positional arguments: 'id', 'name', 'party', and 'is_write_in'"),
    ),
    # id is not a string
    (
        {
            "id": 1,
            "name": [
                "Anthony Alpha",
            ],
            "party": [],
            "is_write_in": False,
        },
        raises(TypeError, match = "Field 'id' is not of type 'str'"),
    ),
    # name is not a list
    (
        {
            "id": "candidate-contest-1--candidate-1",
            "name": "Anthony Alpha",
            "party": [],
            "is_write_in": False,
        },
        raises(TypeError, match = "Field 'name' is not of type 'List'"),
    ),
    # Contents of 'name' are not all strings
    (
        {
            "id": "candidate-contest-1--candidate-1",
            "name": [
                "Anthony Alpha",
                { "name": "Betty Beta" },
            ],
            "party": [],
            "is_write_in": False,
        },
        raises(TypeError, match = "Values in field 'name' are not all of type 'str'"),
    ),
    # party is not a list
    (
        {
            "id": "candidate-contest-1--candidate-1",
            "name": [
                "Anthony Alpha",
            ],
            "party": "",
            "is_write_in": False,
        },
        raises(TypeError, match = "Field 'party' is not of type 'List'"),
    ),
    # 'is write-in' is not a boolean
    (
        {
            "id": "candidate-contest-1--candidate-1",
            "name": [
                "Anthony Alpha",
            ],
            "party": [],
            "is_write_in": None,
        },
        raises(TypeError, match = "Field 'is_write_in' is not of type 'bool'"),
    ),
]


@pytest.mark.parametrize("data, raises", CANDIDATE_CHOICE_TESTS)
def test_candidate_choice(data, raises):
    with raises:
        item = CandidateChoiceData(**data)


def test_candidate_choice_fields():
    data = {
        "id": "candidate-contest-1--candidate-1",
        "name": [
            "Anthony Alpha",
            "Betty Beta",
        ],
        "party": [
            {
                "name": "Lepton Party",
                "abbreviation": "LEP",
            },
        ],
        "is_write_in": False,
    }
    item = CandidateChoiceData(**data)
    assert item.id == data["id"]
    assert item.name == data["name"]
    # Not the same type: data model converts each party to an object
    assert item.party != data["party"]
    # Lengths and fields are the same.
    assert len(item.party) == len(data["party"])
    assert all(isinstance(_, PartyData) for _ in item.party)
    for actual, expected in zip(item.party, data["party"]):
        actual = asdict(actual)
        assert actual == expected
    assert item.is_write_in == data["is_write_in"]
