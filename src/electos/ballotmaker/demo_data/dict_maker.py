import json
from pathlib import Path
from pprint import pprint

from electos.datamodels.nist.indexes.element_index import ElementIndex
from electos.datamodels.nist.models.edf import ElectionReport

edf = Path("/Users/neil/repos/BallotLabFork/tests/june_test_case.json")
edf_data = json.loads(edf.read_text())
election_report = ElectionReport(**edf_data)
index = ElementIndex(election_report, "ElectionResults")

gp_units = {}
offices = {}
parties = {}


def get_gp_units_dict(gp_units: dict) -> int:
    for count, gp_unit in enumerate(
        index.by_type("ElectionResults.ReportingUnit"), start=1
    ):
        gp_unit_id = gp_unit.model__id
        gp_unit_name = gp_unit.name.text[0].content
        # gp_unit_type = gp_unit.type
        print(f" '{gp_unit_id}': '{gp_unit_name}'")
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


print("# Dictionary of GPUnit = id: name")
print(f"Found {get_gp_units_dict(gp_units)} GPUnits:")
pprint(gp_units)

print("# Dictionary of Office = id: name")
print(f"Found {get_offices_dict(offices)} offices:")
pprint(offices)

print("# Dictionary of Party = id: (name, abbreviation)")
print(f"Found {get_parties_dict(parties)} parties:")
pprint(parties)

# generate the list of Persons
print("# Dictionary of People = id: (first name, last name)")
print("people = {")
for person in index.by_type("ElectionResults.Person"):
    person_id = person.model__id
    first_name = person.first_name
    last_name = person.last_name
    print(f"    '{person_id}': ('{first_name}','{last_name}'),")
print("}")

print("# Dictionary of CandidateContest")
for candidate_contest in index.by_type("ElectionResults.CandidateContest"):
    can_contest_id = candidate_contest.model__id
    can_contest_name = candidate_contest.name
    # office_ids could contain multiple items
    office_ids = candidate_contest.office_ids
    contest_offices = [offices[id] for id in office_ids]
    vote_variation = candidate_contest.vote_variation
    votes_allowed = candidate_contest.votes_allowed
    election_district = gp_units[candidate_contest.election_district_id]
    print(
        f" '{can_contest_id}': ('{can_contest_name}','{contest_offices}', '{vote_variation}', {votes_allowed}, '{election_district}'),"
    )
print("}")
