from dataclasses import dataclass, field
from typing import List


@dataclass
class CandidateContestData:
    """Retrieve candidate contest data from a dict"""

    _can_con: dict = field(repr=False)
    # fields retrieved from the dict
    contest_id: str = field(init=False)
    contest_title: str = field(init=False)
    votes_allowed: int = field(init=False)
    district: str = field(init=False)
    candidates: list = field(default_factory=list, init=False, repr=True)

    def __post_init__(self):
        self.contest_id = self._can_con["id"]
        self.contest_title = self._can_con["title"]
        self.votes_allowed = self._can_con["votes_allowed"]
        self.district = self._can_con["district"]
        _candidates = self._can_con["candidates"]
        for candidate_data in _candidates:
            self.candidates.append(CandidateData(candidate_data))


@dataclass
class CandidateData:
    _can_data: dict = field(repr=False)
    candidate_id: str = "no_id_provided"
    candidate_name: str = field(init=False)
    candidate_party: str = field(init=False)
    candidate_party_abbr: str = field(init=False)

    def __post_init__(self):
        self.candidate_name = self._can_data["name"]
        party_dict = self._can_data["party"]
        self.candidate_party = party_dict["name"]
        self.candidate_party_abbr = party_dict["abbreviation"]


if __name__ == "__main__":
    from electos.ballotmaker.demo_data import spacetown_data

    can_con_data_1 = CandidateContestData(spacetown_data.can_con_1)
    print(can_con_data_1)
    can_con_data_2 = CandidateContestData(spacetown_data.can_con_2)
    print(can_con_data_2)
