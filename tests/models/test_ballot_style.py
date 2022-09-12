import pytest

from pytest import raises
from contextlib import nullcontext as raises_none

from dataclasses import asdict

from electos.ballotmaker.data.models import (
    BallotMeasureContestData,
    BallotStyleData,
    CandidateContestData,
)


# Tests

BALLOT_STYLE_TESTS = [
    # Single candidate contest
    (
        {
            "id": "precinct_2_spacetown",
            "scopes": [
                "spacetown-precinct",
            ],
            "contests": [
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
                                "Spencer Cogswell"
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
            ],
        },
        raises_none(),
    ),
    # Single ballot measure contest
    (
        {
            "id": "precinct_2_spacetown",
            "scopes": [
                "spacetown-precinct",
            ],
            "contests": [
                {
                    "id": "ballot-measure-1",
                    "type": "ballot measure",
                    "title": "Ballot Measure #1",
                    "district": "Spacetown",
                    "text": "Ballot measure text",
                    "choices": [
                        {
                            "id": "ballot-measure-1--yes",
                            "choice": "yes",
                        },
                        {
                            "id": "ballot-measure-1--no",
                            "choice": "no",
                        },
                    ],
                },
            ],
        },
        raises_none(),
    ),
    # Multiple contests, conventional order
    (
        {
            "id": "precinct_2_spacetown",
            "scopes": [
                "spacetown-precinct",
            ],
            "contests": [
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
                                "Spencer Cogswell"
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
                {
                    "id": "candidate-contest-2",
                    "type": "candidate",
                    "title": "President of the United States",
                    "district": "United States of America",
                    "vote_type": "plurality",
                    "votes_allowed": 1,
                    "candidates": [
                        {
                            "id": "candidate-contest-2--candidate-1",
                            "name": [
                                "Anthony Alpha",
                                "Betty Beta"
                            ],
                            "party": [
                                {
                                    "name": "The Lepton Party",
                                    "abbreviation": "LEP"
                                }
                            ],
                            "is_write_in": False,
                        },
                        {
                            "id": "candidate-contest-2--candidate-2",
                            "name": [
                                "Gloria Gamma",
                                "David Delta"
                            ],
                            "party": [
                                {
                                    "name": "The Hadron Party of Farallon",
                                    "abbreviation": "HAD"
                                }
                            ],
                            "is_write_in": False,
                        },
                    ],
                },
                {
                    "id": "ballot-measure-1",
                    "type": "ballot measure",
                    "title": "Ballot Measure #1",
                    "district": "Spacetown",
                    "text": "Ballot measure text",
                    "choices": [
                        {
                            "id": "ballot-measure-1--yes",
                            "choice": "yes",
                        },
                        {
                            "id": "ballot-measure-1--no",
                            "choice": "no",
                        },
                    ],
                },
            ],
        },
        raises_none(),
    ),
    # Multiple contests, candidates and write-ins intermingled
    (
        {
            "id": "precinct_2_spacetown",
            "scopes": [
                "spacetown-precinct",
            ],
            "contests": [
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
                                "Spencer Cogswell"
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
                {
                    "id": "ballot-measure-1",
                    "type": "ballot measure",
                    "title": "Ballot Measure #1",
                    "district": "Spacetown",
                    "text": "Ballot measure text",
                    "choices": [
                        {
                            "id": "ballot-measure-1--yes",
                            "choice": "yes",
                        },
                        {
                            "id": "ballot-measure-1--no",
                            "choice": "no",
                        },
                    ],
                },
                {
                    "id": "candidate-contest-2",
                    "type": "candidate",
                    "title": "President of the United States",
                    "district": "United States of America",
                    "vote_type": "plurality",
                    "votes_allowed": 1,
                    "candidates": [
                        {
                            "id": "candidate-contest-2--candidate-1",
                            "name": [
                                "Anthony Alpha",
                                "Betty Beta"
                            ],
                            "party": [
                                {
                                    "name": "The Lepton Party",
                                    "abbreviation": "LEP"
                                }
                            ],
                            "is_write_in": False,
                        },
                        {
                            "id": "candidate-contest-2--candidate-2",
                            "name": [
                                "Gloria Gamma",
                                "David Delta"
                            ],
                            "party": [
                                {
                                    "name": "The Hadron Party of Farallon",
                                    "abbreviation": "HAD"
                                }
                            ],
                            "is_write_in": False,
                        },
                    ],
                },
            ],
        },
        raises_none(),
    ),
    # Empty contests
    pytest.param(
        {
            "id": "precinct_2_spacetown",
            "scopes": [
                "spacetown-precinct",
            ],
            "contests": [],
        },
        raises(ValueError, match = "'contests' cannot be empty"),
        marks = pytest.mark.xfail(reason = "Empty 'contest' list"),
    ),
    # Missing id
    (
        {
            "scopes": [
                "spacetown-precinct",
            ],
            "contests": [
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
                                "Spencer Cogswell"
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
            ],
        },
        raises(TypeError, match = "1 required positional argument: 'id'"),
    ),
    # Missing scopes
    (
        {
            "id": "precinct_2_spacetown",
            "contests": [
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
                                "Spencer Cogswell"
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
            ],
        },
        raises(TypeError, match = "1 required positional argument: 'scopes'"),
    ),
    # Missing contests
    (
        {
            "id": "precinct_2_spacetown",
            "scopes": [
                "spacetown-precinct",
            ],
        },
        raises(TypeError, match = "1 required positional argument: 'contests'"),
    ),
    # Empty object
    (
        {},
        raises(TypeError, match = "3 required positional arguments: 'id', 'scopes', and 'contests'"),
    ),
    # contests is not a list
    (
        {
            "id": "precinct_2_spacetown",
            "scopes": [
                "spacetown-precinct",
            ],
            "contests": {},
        },
        raises(TypeError, match = "Field 'contests' is not of type 'List'"),
    ),
    # Contest is not a dict
    (
        {
            "id": "precinct_2_spacetown",
            "scopes": [
                "spacetown-precinct",
            ],
            "contests": [[]],
        },
        raises(TypeError, match = "Contest is not a dictionary"),
    ),
    # Contest has no type
    (
        {
            "id": "precinct_2_spacetown",
            "scopes": [
                "spacetown-precinct",
            ],
            "contests": [{}],
        },
        raises(KeyError, match = "Contest has no 'type' field"),
    ),
    # Unhandled contest type
    (
        {
            "id": "precinct_2_spacetown",
            "scopes": [
                "spacetown-precinct",
            ],
            "contests": [{ "type": "" }],
        },
        raises(ValueError, match = "Unhandled contest type: ''"),
    ),
    # Ballot measure contest
    (
        {
            "id": "precinct_2_spacetown",
            "scopes": [
                "spacetown-precinct",
            ],
            "contests": [{ "type": BallotStyleData.BALLOT_MEASURE }],
        },
        raises(TypeError, match = "missing 5 required positional arguments: 'id', 'title', 'district', 'text', and 'choices'"),
    ),
    # Candidate contest
    (
        {
            "id": "precinct_2_spacetown",
            "scopes": [
                "spacetown-precinct",
            ],
            "contests": [{ "type": BallotStyleData.CANDIDATE }],
        },
        raises(TypeError, match = "missing 6 required positional arguments: 'id', 'title', 'district', 'vote_type', 'votes_allowed', and 'candidates'"),
    ),
]


@pytest.mark.parametrize("data, raises", BALLOT_STYLE_TESTS)
def test_ballot_style(data, raises):
    with raises:
        item = BallotStyleData(**data)


def test_ballot_style_fields():
    data = {
        "id": "precinct_2_spacetown",
        "scopes": [
            "spacetown-precinct",
        ],
        "contests": [
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
                            "Spencer Cogswell"
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
            {
                "id": "ballot-measure-1",
                "type": "ballot measure",
                "title": "Ballot Measure #1",
                "district": "Spacetown",
                "text": "Ballot measure text",
                "choices": [
                    {
                        "id": "ballot-measure-1--yes",
                        "choice": "yes",
                    },
                    {
                        "id": "ballot-measure-1--no",
                        "choice": "no",
                    },
                ],
            },
        ],
    }
    item = BallotStyleData(**data)
    assert item.id == data["id"]
    assert item.scopes == data["scopes"]
    # Not the same type: data model converts each party to an object
    assert item.contests != data["contests"]
    # Lengths are the same.
    assert len(item.contests) == len(data["contests"])
    # Types are mixed
    assert isinstance(item.contests[0], CandidateContestData)
    assert isinstance(item.contests[1], BallotMeasureContestData)
    for actual, expected in zip(item.contests, data["contests"]):
        actual = asdict(actual)
        assert actual == expected
