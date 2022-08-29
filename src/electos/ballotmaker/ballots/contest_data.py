from dataclasses import dataclass, field
from typing import List


@dataclass
class BallotMeasureData:
    """Retrieve ballot measure contest data from a dict"""

    _b_measure_con: dict = field(repr=False)
    id: str = field(init=False)
    title: str = field(init=False)
    district: str = field(init=False)
    text: str = field(init=False)
    choices: list = field(default_factory=list, init=False, repr=True)

    def __post_init__(self):
        self.id = "no_id_provided"
        self.title = self._b_measure_con["title"]
        self.district = self._b_measure_con["district"]
        self.text = self._b_measure_con["text"]
        self.choices = self._b_measure_con["choices"]
        # for choice_data in _choices:
        #     self.choices.append(ChoiceData(choice_data))


@dataclass
class ChoiceData:
    _choice_data: dict = field(repr=False)
    id: str = "no_id_provided"
    label: str = field(init=False)

    def __post_init__(self):
        self.label = "no label provided"


@dataclass
class CandidateContestData:
    """Retrieve candidate contest data from a dict"""

    _can_con: dict = field(repr=False)
    # fields retrieved from the dict
    id: str = field(init=False)
    title: str = field(init=False)
    votes_allowed: int = field(init=False)
    district: str = field(init=False)
    candidates: list = field(default_factory=list, init=False, repr=True)

    def __post_init__(self):
        self.id = self._can_con["id"]
        self.title = self._can_con["title"]
        self.votes_allowed = self._can_con["votes_allowed"]
        self.district = self._can_con["district"]
        _candidates = self._can_con["candidates"]
        for candidate_data in _candidates:
            self.candidates.append(CandidateData(candidate_data))


@dataclass
class CandidateData:
    _can_data: dict = field(repr=False)
    id: str = "no_id_provided"
    name: str = field(init=False)
    party: str = field(init=False)
    party_abbr: str = field(init=False)

    def __post_init__(self):
        self.name = self._can_data["name"]
        party_dict = self._can_data["party"]
        self.party = party_dict["name"]
        self.party_abbr = party_dict["abbreviation"]


if __name__ == "__main__":  # pragma: no cover
    from electos.ballotmaker.demo_data import spacetown_data

    can_con_data_1 = CandidateContestData(spacetown_data.can_con_1)
    print(can_con_data_1)
    can_con_data_2 = CandidateContestData(spacetown_data.can_con_2)
    print(can_con_data_2)
    b_measure_data_1 = BallotMeasureData(spacetown_data.ballot_measure_1)
    print(b_measure_data_1)
