"""Ballot data models."""

from dataclasses import dataclass
from typing import List


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


# --- Ballot contest data models


@dataclass
class BallotChoiceData:

    """Data for ballot measure selections."""

    id: str
    choice: str


    def __post_init__(self):
        _check_type(self, "id", str)
        _check_type(self, "choice", str)
