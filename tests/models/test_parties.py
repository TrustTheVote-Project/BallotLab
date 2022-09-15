import pytest

from pytest import raises
from contextlib import nullcontext as raises_none

from electos.ballotmaker.data.models import (
    PartyData,
)


# Tests

PARTY_TESTS = [
    (
        {
            "name": "Un-Committed Party",
            "abbreviation": "UCP",
        },
        raises_none(),
    ),
    # Missing name
    (
        {
            "abbreviation": "UCP",
        },
        raises(TypeError, match = "required positional argument: 'name'"),
    ),
    # Missing abbreviation
    (
        {
            "name": "Un-Committed Party",
        },
        raises(TypeError, match = "required positional argument: 'abbreviation'"),
    ),
    # Empty object
    (
        {},
        raises(TypeError, match = "2 required positional arguments: 'name' and 'abbreviation'"),
    ),
    # name is not a string
    (
        {
            "name": 1,
            "abbreviation": "UCP",
        },
        raises(TypeError, match = "Field 'name' is not of type 'str'"),
    ),
    # abbreviation is not a string
    (
        {
            "name": "Un-Committed Party",
            "abbreviation": [],
        },
        raises(TypeError, match = "Field 'abbreviation' is not of type 'str'"),
    ),
]


@pytest.mark.parametrize("data, raises", PARTY_TESTS)
def test_party(data, raises):
    with raises:
        item = PartyData(**data)


def test_party_fields():
    data = {
        "name": "Un-Committed Party",
        "abbreviation": "UCP",
    }
    item = PartyData(**data)
    assert item.name == data["name"]
    assert item.abbreviation == data["abbreviation"]
