import pytest

from pytest import raises
from contextlib import nullcontext as raises_none

from electos.ballotmaker.data.models import (
    BallotChoiceData,
    BallotMeasureContestData,
)


# Tests

BALLOT_MEASURE_CONTEST_TESTS = [
    # Two choices
    (
        {
            "id": "ballot-measure-1",
            "type": "ballot-measure",
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
        raises_none(),
    ),
    # Empty choices
    pytest.param(
        {
            "id": "ballot-measure-1",
            "type": "ballot-measure",
            "title": "Ballot Measure #1",
            "district": "Spacetown",
            "text": "Ballot measure text",
            "choices": [],
        },
        raises(ValueError, match = "Insufficient number of ballot choices"),
        marks = pytest.mark.xfail(reason = "Empty 'choices' list"),
    ),
    # Only one choice
    pytest.param(
        {
            "id": "ballot-measure-1",
            "type": "ballot-measure",
            "title": "Ballot Measure #1",
            "district": "Spacetown",
            "text": "Ballot measure text",
            "choices": [
                {
                    "id": "ballot-measure-1--yes",
                    "choice": "yes",
                },
            ],
        },
        raises(ValueError, match = "Insufficient number of ballot choices"),
        marks = pytest.mark.xfail(reason = "Only one choice in 'choices' list"),
    ),
    # One choice, duplicated
    pytest.param(
        {
            "id": "ballot-measure-1",
            "type": "ballot-measure",
            "title": "Ballot Measure #1",
            "district": "Spacetown",
            "text": "Ballot measure text",
            "choices": [
                {
                    "id": "ballot-measure-1--yes",
                    "choice": "yes",
                },
                {
                    "id": "ballot-measure-1--yes",
                    "choice": "yes",
                },
            ],
        },
        raises(ValueError, match = "Duplicate ballot choices"),
        marks = pytest.mark.xfail(reason = "Duplicate ballot choices"),
    ),
    # Missing id
    (
        {
            "type": "ballot-measure",
            "title": "Ballot Measure #1",
            "district": "Spacetown",
            "text": "Ballot measure text",
            "choices": [],
        },
        raises(TypeError, match = "required positional argument: 'id'"),
    ),
    # Missing type
    (
        {
            "id": "ballot-measure-1",
            "title": "Ballot Measure #1",
            "district": "Spacetown",
            "text": "Ballot measure text",
            "choices": [],
        },
        raises(TypeError, match = "required positional argument: 'type'"),
    ),
    # Missing title
    (
        {
            "type": "ballot-measure",
            "id": "ballot-measure-1",
            "district": "Spacetown",
            "text": "Ballot measure text",
            "choices": [],
        },
        raises(TypeError, match = "required positional argument: 'title'"),
    ),
    # Missing district
    (
        {
            "id": "ballot-measure-1",
            "type": "ballot-measure",
            "title": "Ballot Measure #1",
            "text": "Ballot measure text",
            "choices": [],
        },
        raises(TypeError, match = "required positional argument: 'district'"),
    ),
    # Missing text
    (
        {
            "id": "ballot-measure-1",
            "type": "ballot-measure",
            "title": "Ballot Measure #1",
            "district": "Spacetown",
            "choices": [],
        },
        raises(TypeError, match = "required positional argument: 'text'"),
    ),
    # Missing choices
    (
        {
            "id": "ballot-measure-1",
            "type": "ballot-measure",
            "title": "Ballot Measure #1",
            "district": "Spacetown",
            "text": "Ballot measure text",
        },
        raises(TypeError, match = "required positional argument: 'choices'"),
    ),
    # Empty object
    (
        {},
        raises(TypeError, match = "required positional arguments: 'id', 'type', 'title', 'district', 'text', and 'choices'"),
    ),
    # id is not a string
    (
        {
            "id": 1,
            "type": "ballot-measure",
            "title": "Ballot Measure #1",
            "district": "Spacetown",
            "text": "Ballot measure text",
            "choices": [],
        },
        raises(TypeError, match = "Field 'id' is not of type 'str'"),
    ),
    # type is not a string
    (
        {
            "id": "ballot-measure-1",
            "type": 1,
            "title": "Ballot Measure #1",
            "district": "Spacetown",
            "text": "Ballot measure text",
            "choices": [],
        },
        raises(TypeError, match = "Field 'type' is not of type 'str'"),
    ),
    # title is not a string
    (
        {
            "id": "ballot-measure-1",
            "type": "ballot-measure",
            "title": 2,
            "district": "Spacetown",
            "text": "Ballot measure text",
            "choices": [],
        },
        raises(TypeError, match = "Field 'title' is not of type 'str'"),
    ),
    # district is not a string
    (
        {
            "id": "ballot-measure-1",
            "type": "ballot-measure",
            "title": "Ballot Measure #1",
            "district": [],
            "text": "Ballot measure text",
            "choices": [],
        },
        raises(TypeError, match = "Field 'district' is not of type 'str'"),
    ),
    # text is not a string
    (
        {
            "id": "ballot-measure-1",
            "type": "ballot-measure",
            "title": "Ballot Measure #1",
            "district": "Spacetown",
            "text": {},
            "choices": [],
        },
        raises(TypeError, match = "Field 'text' is not of type 'str'"),
    ),
    # choices is not a list
    (
        {
            "id": "ballot-measure-1",
            "type": "ballot-measure",
            "title": "Ballot Measure #1",
            "district": "Spacetown",
            "text": "Ballot measure text",
            "choices": {},
        },
        raises(TypeError, match = "Field 'choices' is not of type 'List'"),
    ),
    # choice is not a dictionary that can convert to a BallotChoiceData
    (
        {
            "id": "ballot-measure-1",
            "type": "ballot-measure",
            "title": "Ballot Measure #1",
            "district": "Spacetown",
            "text": "Ballot measure text",
            "choices": [{}],
        },
        raises(TypeError, match = "missing 2 required positional arguments: 'id' and 'choice'"),
    ),
]


@pytest.mark.parametrize("data, raises", BALLOT_MEASURE_CONTEST_TESTS)
def test_ballot_measure_contest(data, raises):
    with raises:
        item = BallotMeasureContestData(**data)


def test_ballot_measure_contest_fields():
    data = {
        "id": "ballot-measure-1",
        "type": "ballot-measure",
        "title": "Ballot Measure #1",
        "district": "Spacetown",
        "text": "Ballot measure text",
        "choices": [
            {
                "id": "ballot-measure-1--yes",
                "choice": "yes"
            },
            {
                "id": "ballot-measure-1--no",
                "choice": "no"
            },
        ]
    }
    item = BallotMeasureContestData(**data)
    # Scalar fields match
    assert item.id == data["id"]
    assert item.type == data["type"]
    assert item.title == data["title"]
    assert item.district == data["district"]
    assert item.text == data["text"]
    # Not the same type: data model converts each party to an object
    assert item.choices != data["choices"]
    # Scalar field values
    assert item.type == "ballot-measure"
    # Lengths and fields are the same.
    assert len(item.choices) == len(data["choices"])
    assert all(isinstance(_, BallotChoiceData) for _ in item.choices)
    for actual, expected in zip(item.choices, data["choices"]):
        assert actual.id == expected["id"]
        assert actual.choice == expected["choice"]
