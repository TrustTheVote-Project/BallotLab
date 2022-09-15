import pytest

from pytest import raises
from contextlib import nullcontext as raises_none

from dataclasses import asdict

from electos.ballotmaker.data.models import (
    BallotStyleData,
    ElectionData,
)


# Tests

ELECTION_TESTS = [
    (
        {
            "name": "General Election",
            "type": "general",
            "start_date": "2024-11-05",
            "end_date": "2024-11-05",
            "ballot_styles": [
                {
                    "id": "precinct_2_spacetown",
                    "scopes": [
                        "spacetown-precinct",
                    ],
                    "contests": [
                        {
                            "id": "candidate-contest-orbit-city-mayor",
                            "title": "Mayor of Orbit City",
                            "type": "candidate",
                            "vote_type": "plurality",
                            "votes_allowed": 1,
                            "district": "Orbit City",
                            "candidates": [
                                {
                                    "id": "candidate-choice-1",
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
            ],
        },
        raises_none()
    ),
    # Empty ballot styles
    pytest.param(
        {
            "name": "General Election",
            "start_date": "2024-11-05",
            "end_date": "2024-11-05",
            "type": "general",
            "ballot_styles": [],
        },
        raises(ValueError, match = "Ballot styles are empty"),
        marks = pytest.mark.xfail(reason = "Empty 'ballot_styles' list")
    ),
    # Missing name
    (
        {
            "start_date": "2024-11-05",
            "end_date": "2024-11-05",
            "type": "general",
            "ballot_styles": [
                {
                    "id": "precinct_2_spacetown",
                    "scopes": [
                        "spacetown-precinct",
                    ],
                    "contests": [
                        {
                            "id": "candidate-contest-orbit-city-mayor",
                            "title": "Mayor of Orbit City",
                            "type": "candidate",
                            "vote_type": "plurality",
                            "votes_allowed": 1,
                            "district": "Orbit City",
                            "candidates": [
                                {
                                    "id": "candidate-choice-1",
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
            ],
        },
        raises(TypeError, match = "required positional argument: 'name'")
    ),
    # Missing type
    (
        {
            "name": "General Election",
            "start_date": "2024-11-05",
            "end_date": "2024-11-05",
            "ballot_styles": [
                {
                    "id": "precinct_2_spacetown",
                    "scopes": [
                        "spacetown-precinct",
                    ],
                    "contests": [
                        {
                            "id": "candidate-contest-orbit-city-mayor",
                            "title": "Mayor of Orbit City",
                            "type": "candidate",
                            "vote_type": "plurality",
                            "votes_allowed": 1,
                            "district": "Orbit City",
                            "candidates": [
                                {
                                    "id": "candidate-choice-1",
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
            ],
        },
        raises(TypeError, match = "required positional argument: 'type'")
    ),
    # Missing start date
    (
        {
            "name": "General Election",
            "end_date": "2024-11-05",
            "type": "general",
            "ballot_styles": [
                {
                    "id": "precinct_2_spacetown",
                    "scopes": [
                        "spacetown-precinct",
                    ],
                    "contests": [
                        {
                            "id": "candidate-contest-orbit-city-mayor",
                            "title": "Mayor of Orbit City",
                            "type": "candidate",
                            "vote_type": "plurality",
                            "votes_allowed": 1,
                            "district": "Orbit City",
                            "candidates": [
                                {
                                    "id": "candidate-choice-1",
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
            ],
        },
        raises(TypeError, match = "required positional argument: 'start_date'")
    ),
    # Missing end date
    (
        {
            "name": "General Election",
            "start_date": "2024-11-05",
            "type": "general",
            "ballot_styles": [
                {
                    "id": "precinct_2_spacetown",
                    "scopes": [
                        "spacetown-precinct",
                    ],
                    "contests": [
                        {
                            "id": "candidate-contest-orbit-city-mayor",
                            "title": "Mayor of Orbit City",
                            "type": "candidate",
                            "vote_type": "plurality",
                            "votes_allowed": 1,
                            "district": "Orbit City",
                            "candidates": [
                                {
                                    "id": "candidate-choice-1",
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
            ],
        },
        raises(TypeError, match = "required positional argument: 'end_date'")
    ),
    # Missing ballot styles
    (
        {
            "name": "General Election",
            "start_date": "2024-11-05",
            "end_date": "2024-11-05",
            "type": "general",
        },
        raises(TypeError, match = "required positional argument: 'ballot_styles'")
    ),
    # Empty object
    (
        {},
        raises(TypeError, match = "5 required positional arguments: 'name', 'type', 'start_date', 'end_date', and 'ballot_styles'")
    ),
    # name is not a string
    (
        {
            "name": 1,
            "type": "general",
            "start_date": "2024-11-05",
            "end_date": "2024-11-05",
            "ballot_styles": [],
        },
        raises(TypeError, match = "Field 'name' is not of type 'str'"),
    ),
    # type is not a string
    (
        {
            "name": "General Election",
            "type": 2,
            "start_date": "2024-11-05",
            "end_date": "2024-11-05",
            "ballot_styles": [],
        },
        raises(TypeError, match = "Field 'type' is not of type 'str'"),
    ),
    # 'start date' is not a string
    (
        {
            "name": "General Election",
            "type": "general",
            "start_date": 3,
            "end_date": "2024-11-05",
            "ballot_styles": [],
        },
        raises(TypeError, match = "Field 'start_date' is not of type 'str'"),
    ),
    # 'end date' is not a string
    (
        {
            "name": "General Election",
            "type": "general",
            "start_date": "2024-11-05",
            "end_date": 4,
            "ballot_styles": [],
        },
        raises(TypeError, match = "Field 'end_date' is not of type 'str'"),
    ),
    # 'ballot styles' is not a list
    (
        {
            "name": "General Election",
            "type": "general",
            "start_date": "2024-11-05",
            "end_date": "2024-11-05",
            "ballot_styles": {},
        },
        raises(TypeError, match = "Field 'ballot_styles' is not of type 'List'"),
    ),
]


@pytest.mark.parametrize("data, raises", ELECTION_TESTS)
def test_election(data, raises):
    with raises:
        item = ElectionData(**data)


def test_election_fields():
    data = {
        "name": "General Election",
        "type": "general",
        "start_date": "2024-11-05",
        "end_date": "2024-11-05",
        "ballot_styles": [
            {
                "id": "precinct_2_spacetown",
                "scopes": [
                    "spacetown-precinct",
                ],
                "contests": [
                    {
                        "id": "candidate-contest-orbit-city-mayor",
                        "title": "Mayor of Orbit City",
                        "type": "candidate",
                        "vote_type": "plurality",
                        "votes_allowed": 1,
                        "district": "Orbit City",
                        "candidates": [
                            {
                                "id": "candidate-choice-1",
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
        ],
    }
    item = ElectionData(**data)
    # Scalar fields match
    assert item.name == data["name"]
    assert item.type == data["type"]
    assert item.start_date == data["start_date"]
    assert item.end_date == data["end_date"]
    # Not the same type: data model converts each party to an object
    assert item.ballot_styles != data["ballot_styles"]
    # Lengths and fields are the same.
    assert len(item.ballot_styles) == len(data["ballot_styles"])
    assert all(isinstance(_, BallotStyleData) for _ in item.ballot_styles)
    for actual, expected in zip(item.ballot_styles, data["ballot_styles"]):
        actual = asdict(actual)
        assert actual == expected
