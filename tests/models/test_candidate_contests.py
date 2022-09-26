import pytest

from pytest import raises
from contextlib import nullcontext as raises_none

from dataclasses import asdict

from electos.ballotmaker.data.models import (
    CandidateChoiceData,
    CandidateContestData,
)


# Tests

CANDIDATE_CONTEST_TESTS = [
    # Single candidate
    (
        {
            "id": "candidate-contest-1",
            "type": "candidate",
            "title": "Mayor of Orbit City",
            "district": "Orbit City",
            "vote_type": "plurality",
            "votes_allowed": 1,
            "candidates": [
                {
                    "id": "candidate-contest-1--candidate-1",
                    "name": [
                        "Spencer Cogswell",
                    ],
                    "party": [
                        {
                            "name": "The Hadron Party of Farallon",
                            "abbreviation": "HAD",
                        },
                    ],
                    "is_write_in": False,
                },
            ],
        },
        raises_none(),
    ),
    # Multiple candidates
    (
        {
            "id": "candidate-contest-1",
            "type": "candidate",
            "title": "Mayor of Orbit City",
            "district": "Orbit City",
            "vote_type": "plurality",
            "votes_allowed": 1,
            "candidates": [
                {
                    "id": "candidate-contest-1--candidate-1",
                    "name": [
                        "Cosmo Spacely",
                    ],
                    "party": [
                        {
                            "name": "The Lepton Partyn",
                            "abbreviation": "LEP",
                        },
                    ],
                    "is_write_in": False,
                },
                {
                    "id": "candidate-contest-1--candidate-2",
                    "name": [
                        "Spencer Cogswell",
                    ],
                    "party": [
                        {
                            "name": "The Hadron Party of Farallon",
                            "abbreviation": "HAD",
                        },
                    ],
                    "is_write_in": False,
                },
            ],
        },
        raises_none(),
    ),
    # Write-in
    (
        {
            "id": "candidate-contest-1",
            "type": "candidate",
            "title": "Mayor of Orbit City",
            "district": "Orbit City",
            "vote_type": "plurality",
            "votes_allowed": 1,
            "candidates": [
                {
                    "id": "candidate-contest-1--write-in-1",
                    "name": [],
                    "party": [],
                    "is_write_in": True,
                },
            ],
        },
        raises_none(),
    ),
    # Candidate + write-in
    (
        {
            "id": "candidate-contest-1",
            "type": "candidate",
            "title": "Mayor of Orbit City",
            "district": "Orbit City",
            "vote_type": "plurality",
            "votes_allowed": 1,
            "candidates": [
                {
                    "id": "candidate-contest-1--candidate-1",
                    "name": [
                        "Spencer Cogswell",
                    ],
                    "party": [
                        {
                            "name": "The Hadron Party of Farallon",
                            "abbreviation": "HAD",
                        }
                    ],
                    "is_write_in": False,
                },
                {
                    "id": "candidate-contest-1--write-in-1",
                    "name": [],
                    "party": [],
                    "is_write_in": True,
                },
            ],
        },
        raises_none(),
    ),
    # Empty candidates
    pytest.param(
        {
            "id": "candidate-contest-1",
            "type": "candidate",
            "title": "Mayor of Orbit City",
            "district": "Orbit City",
            "vote_type": "plurality",
            "votes_allowed": 1,
            "candidates": [],
        },
        raises(ValueError, match = "Insufficient number of candidates"),
        marks = pytest.mark.xfail(reason = "Empty 'candidates' list"),
    ),
    # Single candidate, duplicated
    pytest.param(
        {
            "id": "candidate-contest-1",
            "type": "candidate",
            "title": "Mayor of Orbit City",
            "district": "Orbit City",
            "vote_type": "plurality",
            "votes_allowed": 1,
            "candidates": [
                {
                    "id": "candidate-contest-1--candidate-1",
                    "name": [
                        "Spencer Cogswell",
                    ],
                    "party": [
                        {
                            "name": "The Hadron Party of Farallon",
                            "abbreviation": "HAD",
                        },
                    ],
                    "is_write_in": False,
                },
                {
                    "id": "candidate-contest-1--candidate-1",
                    "name": [
                        "Spencer Cogswell",
                    ],
                    "party": [
                        {
                            "name": "The Hadron Party of Farallon",
                            "abbreviation": "HAD",
                        },
                    ],
                    "is_write_in": False,
                },
            ],
        },
        raises(ValueError, match = "Duplicate candidate"),
        marks = pytest.mark.xfail(reason = "Duplicate candidate"),
    ),
    # Missing id
    (
        {
            "type": "candidate",
            "title": "Mayor of Orbit City",
            "district": "Orbit City",
            "vote_type": "plurality",
            "votes_allowed": 1,
            "candidates": [
                {
                    "id": "candidate-contest-1--candidate-1",
                    "name": [
                        "Spencer Cogswell",
                    ],
                    "party": [
                        {
                            "name": "The Hadron Party of Farallon",
                            "abbreviation": "HAD"
                        },
                    ],
                    "is_write_in": False,
                },
            ],
        },
        raises(TypeError, match = "required positional argument: 'id'"),
    ),
    # Missing type
    (
        {
            "id": "candidate-contest-1",
            "title": "Mayor of Orbit City",
            "district": "Orbit City",
            "vote_type": "plurality",
            "votes_allowed": 1,
            "candidates": [
                {
                    "id": "candidate-contest-1--candidate-1",
                    "name": [
                        "Spencer Cogswell",
                    ],
                    "party": [
                        {
                            "name": "The Hadron Party of Farallon",
                            "abbreviation": "HAD"
                        },
                    ],
                    "is_write_in": False,
                },
            ],
        },
        raises(TypeError, match = "required positional argument: 'type'"),
    ),
    # Missing title
    (
        {
            "id": "candidate-contest-1",
            "type": "candidate",
            "district": "Orbit City",
            "vote_type": "plurality",
            "votes_allowed": 1,
            "candidates": [
                {
                    "id": "candidate-contest-1--candidate-1",
                    "name": [
                        "Spencer Cogswell",
                    ],
                    "party": [
                        {
                            "name": "The Hadron Party of Farallon",
                            "abbreviation": "HAD"
                        },
                    ],
                    "is_write_in": False,
                },
            ],
        },
        raises(TypeError, match = "required positional argument: 'title'"),
    ),
    # Missing district
    (
        {
            "id": "candidate-contest-1",
            "type": "candidate",
            "title": "Mayor of Orbit City",
            "vote_type": "plurality",
            "votes_allowed": 1,
            "candidates": [
                {
                    "id": "candidate-contest-1--candidate-1",
                    "name": [
                        "Spencer Cogswell",
                    ],
                    "party": [
                        {
                            "name": "The Hadron Party of Farallon",
                            "abbreviation": "HAD"
                        },
                    ],
                    "is_write_in": False,
                },
            ],
        },
        raises(TypeError, match = "required positional argument: 'district'"),
    ),
    # Missing vote type
    (
        {
            "id": "candidate-contest-1",
            "type": "candidate",
            "title": "Mayor of Orbit City",
            "district": "Orbit City",
            "votes_allowed": 1,
            "candidates": [
                {
                    "id": "candidate-contest-1--candidate-1",
                    "name": [
                        "Spencer Cogswell",
                    ],
                    "party": [
                        {
                            "name": "The Hadron Party of Farallon",
                            "abbreviation": "HAD"
                        },
                    ],
                    "is_write_in": False,
                },
            ],
        },
        raises(TypeError, match = "required positional argument: 'vote_type'"),
    ),
    # Missing votes allowed
    (
        {
            "id": "candidate-contest-1",
            "type": "candidate",
            "title": "Mayor of Orbit City",
            "district": "Orbit City",
            "vote_type": "plurality",
            "candidates": [
                {
                    "id": "candidate-contest-1--candidate-1",
                    "name": [
                        "Spencer Cogswell",
                    ],
                    "party": [
                        {
                            "name": "The Hadron Party of Farallon",
                            "abbreviation": "HAD"
                        },
                    ],
                    "is_write_in": False,
                },
            ],
        },
        raises(TypeError, match = "required positional argument: 'votes_allowed'"),
    ),
    # Missing candidates
    (
        {
            "id": "candidate-contest-1",
            "type": "candidate",
            "title": "Mayor of Orbit City",
            "district": "Orbit City",
            "vote_type": "plurality",
            "votes_allowed": 1,
        },
        raises(TypeError, match = "required positional argument: 'candidates'"),
    ),
    # Empty object
    (
        {},
        raises(TypeError, match = "required positional arguments: 'id', 'type', 'title', 'district', 'vote_type', 'votes_allowed', and 'candidates'"),
    ),
    # id is not a string
    (
        {
            "id": 1,
            "type": "candidate",
            "title": "Mayor of Orbit City",
            "district": "Orbit City",
            "vote_type": "plurality",
            "votes_allowed": 1,
            "candidates": [],
        },
        raises(TypeError, match = "Field 'id' is not of type 'str'"),
    ),
    # type not a string
    (
        {
            "id": "candidate-contest-1",
            "type": 2,
            "title": "Mayor of Orbit City",
            "district": "Orbit City",
            "vote_type": "plurality",
            "votes_allowed": 1,
            "candidates": [],
        },
        raises(TypeError, match = "Field 'type' is not of type 'str'"),
    ),
    # title is not a string
    (
        {
            "id": "candidate-contest-1",
            "type": "candidate",
            "title": 3,
            "district": "Orbit City",
            "vote_type": "plurality",
            "votes_allowed": 1,
            "candidates": [],
        },
        raises(TypeError, match = "Field 'title' is not of type 'str'"),
    ),
    # district is not a string
    (
        {
            "id": "candidate-contest-1",
            "type": "candidate",
            "title": "Mayor of Orbit City",
            "district": 4,
            "vote_type": "plurality",
            "votes_allowed": 1,
            "candidates": [],
        },
        raises(TypeError, match = "Field 'district' is not of type 'str'"),
    ),
    # "vote type" is not a string
    (
        {
            "id": "candidate-contest-1",
            "type": "candidate",
            "title": "Mayor of Orbit City",
            "district": "Orbit City",
            "vote_type": 5,
            "votes_allowed": 1,
            "candidates": [],
        },
        raises(TypeError, match = "Field 'vote_type' is not of type 'str'"),
    ),
    # "votes allowed" not an integer
    (
        {
            "id": "candidate-contest-1",
            "type": "candidate",
            "title": "Mayor of Orbit City",
            "district": "Orbit City",
            "vote_type": "plurality",
            "votes_allowed": "one",
            "candidates": [],
        },
        raises(TypeError, match = "Field 'votes_allowed' is not of type 'int'"),
    ),
    # candidates is not a list
    (
        {
            "id": "candidate-contest-1",
            "type": "candidate",
            "title": "Mayor of Orbit City",
            "district": "Orbit City",
            "vote_type": "plurality",
            "votes_allowed": 1,
            "candidates": {},
        },
        raises(TypeError, match = "Field 'candidates' is not of type 'List'"),
    ),
    # candidate is not a dictionary that can convert to a CandidateChoiceData
    (
        {
            "id": "candidate-contest-1",
            "type": "candidate",
            "title": "Mayor of Orbit City",
            "district": "Orbit City",
            "vote_type": "plurality",
            "votes_allowed": 1,
            "candidates": [{}],
        },
        raises(TypeError, match = "missing 4 required positional arguments: 'id', 'name', 'party', and 'is_write_in'"),
    ),
]


@pytest.mark.parametrize("data, raises", CANDIDATE_CONTEST_TESTS)
def test_candidate_contest(data, raises):
    with raises:
        item = CandidateContestData(**data)


def test_candidate_contest_fields():
    data = {
        "id": "candidate-contest-1",
        "type": "candidate",
        "title": "Mayor of Orbit City",
        "district": "Orbit City",
        "vote_type": "plurality",
        "votes_allowed": 1,
        "candidates": [
            {
                "id": "candidate-contest-1--candidate-1",
                "name": [
                    "Spencer Cogswell",
                ],
                "party": [
                    {
                        "name": "The Hadron Party of Farallon",
                        "abbreviation": "HAD",
                    }
                ],
                "is_write_in": False,
            },
            {
                "id": "candidate-contest-1--write-in-1",
                "name": [],
                "party": [],
                "is_write_in": True,
            },
        ],
    }
    item = CandidateContestData(**data)
    # Scalar fields match
    assert item.id == data["id"]
    assert item.type == data["type"]
    assert item.title == data["title"]
    assert item.vote_type == data["vote_type"]
    assert item.votes_allowed == data["votes_allowed"]
    assert item.district == data["district"]
    # Not the same type: data model converts each party to an object
    assert item.candidates != data["candidates"]
    # Lengths and fields are the same.
    assert len(item.candidates) == len(data["candidates"])
    assert all(isinstance(_, CandidateChoiceData) for _ in item.candidates)
    for actual, expected in zip(item.candidates, data["candidates"]):
        actual = asdict(actual)
        assert actual == expected
