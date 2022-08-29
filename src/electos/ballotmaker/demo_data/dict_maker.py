import json
from pathlib import Path
from pprint import pprint

from electos.datamodels.nist.indexes.element_index import ElementIndex
from electos.datamodels.nist.models.edf import ElectionReport

edf = Path("/Users/neil/repos/BallotLabFork/tests/june_test_case.json")
edf_data = json.loads(edf.read_text())
election_report = ElectionReport(**edf_data)
index = ElementIndex(election_report, "ElectionResults")

candidates = {}
gp_units = {}
offices = {}
parties = {}
people = {}


def get_gp_units_dict(gp_units: dict) -> int:
    for count, gp_unit in enumerate(
        index.by_type("ElectionResults.ReportingUnit"), start=1
    ):
        gp_unit_id = gp_unit.model__id
        gp_unit_name = gp_unit.name.text[0].content
        # gp_unit_type = gp_unit.type
        # print(f" '{gp_unit_id}': '{gp_unit_name}'")
        gp_units[gp_unit_id] = gp_unit_name
    return count


def get_offices_dict(offices: dict) -> int:
    for count, office in enumerate(
        index.by_type("ElectionResults.Office"), start=1
    ):
        office_id = office.model__id
        office_name = office.name.text[0].content
        print(f" '{office_id}': '{office_name}'")
        offices[office_id] = office_name
    return count


def get_parties_dict(parties: dict) -> int:
    for count, party in enumerate(
        index.by_type("ElectionResults.Party"), start=1
    ):
        party_id = party.model__id
        party_name = party.name.text[0].content
        party_abbr = party.abbreviation.text[0].content
        party_value = (party_name, party_abbr)
        print(f" '{party_id}': ('{party_name}, {party_abbr})'")
        parties[party_id] = party_value
    return count


def get_people_dict(people: dict) -> int:
    for count, person in enumerate(
        index.by_type("ElectionResults.Person"), start=1
    ):
        person_id = person.model__id
        first_name = person.first_name
        last_name = person.last_name
        print(f" '{person_id}': {first_name} {last_name},")
        people[person_id] = f"{first_name} {last_name}"
    return count


def get_candidate_dict(candidates: dict) -> int:
    for count, candidate in enumerate(
        index.by_type("ElectionResults.Candidate"), start=1
    ):
        candidate_id = candidate.model__id
        candidate_ballot_name = candidate.ballot_name.text[0].content
        print(f" '{candidate_id}': {candidate_ballot_name},")
        candidates[candidate_id] = candidate_ballot_name
    return count


print("# Dictionary of GPUnit = id: name")
print(f"Found {get_gp_units_dict(gp_units)} GPUnits:")
pprint(gp_units)

print("# Dictionary of Office = id: name")
print(f"Found {get_offices_dict(offices)} offices:")
pprint(offices)

print("# Dictionary of Party = id: (name, abbreviation)")
print(f"Found {get_parties_dict(parties)} parties:")
pprint(parties)

print("# Dictionary of People = id: firstname lastname")
print(f"Found {get_people_dict(people)} people:")
pprint(people)

print("# Dictionary of Candidate")
print(f"Found {get_candidate_dict(candidates)} candidate:")
pprint(candidates)

print("# Dictionary of CandidateContest")
for candidate_contest in index.by_type("ElectionResults.CandidateContest"):
    vote_variation = candidate_contest.vote_variation.value
    if vote_variation == "n-of-m":
        continue
    can_contest_id = candidate_contest.model__id
    can_contest_name = candidate_contest.name
    # office_ids could contain multiple items
    office_ids = candidate_contest.office_ids
    contest_offices = [offices[id] for id in office_ids]
    votes_allowed = candidate_contest.votes_allowed
    election_district = gp_units[candidate_contest.election_district_id]
    contest_index = ElementIndex(candidate_contest, "ElectionResults")
    print(
        f" '{can_contest_id}': ('{can_contest_name}','{contest_offices}', '{vote_variation}', {votes_allowed}, '{election_district}'),"
    )
    print(contest_index)
    for content_selection in contest_index.by_type(
        "ElectionResults.CandidateSelection"
    ):
        print(content_selection.name)
        contest_id = content_selection.model__id

        candidate_ids = content_selection.candidate_ids
        candidate_names = [candidates[c_id] for c_id in candidate_ids]
        print(f"{contest_id} {candidate_names}")
