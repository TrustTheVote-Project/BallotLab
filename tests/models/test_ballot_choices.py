import pytest

from pytest import raises
from contextlib import nullcontext as raises_none

from electos.ballotmaker.data.models import (
    BallotChoiceData,
)


# Tests

BALLOT_CHOICE_TESTS = [
    (
        {
            "id": "ballot-measure-1--yes",
            "choice": "yes",
        },
        raises_none(),
    ),
    # Missing id
    (
        {
            "choice": "yes",
        },
        raises(TypeError, match = "required positional argument: 'id'"),
    ),
    # Missing choice
    (
        {
            "id": "ballot-measure-1--yes",
        },
        raises(TypeError, match = "required positional argument: 'choice'"),
    ),
    # Empty object
    (
        {},
        raises(TypeError, match = "2 required positional arguments: 'id' and 'choice'"),
    ),
    # id is not a string
    (
        {
            "id": 1,
            "choice": "yes",
        },
        raises(TypeError, match = "Field 'id' is not of type 'str'"),
    ),
    # choice is not a string
    (
        {
            "id": "ballot-measure-1--yes",
            "choice": [],
        },
        raises(TypeError, match = "Field 'choice' is not of type 'str'"),
    ),
]


@pytest.mark.parametrize("data, raises", BALLOT_CHOICE_TESTS)
def test_ballot_choice(data, raises):
    with raises:
        item = BallotChoiceData(**data)


def test_ballot_choice_fields():
    data = {
        "id": "ballot-measure-1--yes",
        "choice": "yes"
    }
    item = BallotChoiceData(**data)
    assert item.id == data["id"]
    assert item.choice == data["choice"]
