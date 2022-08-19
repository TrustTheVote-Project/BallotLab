import json
from pathlib import Path

from electos.datamodels.nist.indexes.element_index import ElementIndex
from electos.datamodels.nist.models.edf import ElectionReport

edf = Path("/Users/neil/repos/BallotLabFork/tests/june_test_case.json")
edf_data = json.loads(edf.read_text())
election_report = ElectionReport(**edf_data)
index = ElementIndex(election_report, "ElectionResults")

for party in index.by_type("ElectionResults.Party"):
    party_id = party.model__id
    print(f"'{party_id}'")

# generate the list of Persons
print("people = {")
for person in index.by_type("ElectionResults.Person"):
    person_id = person.model__id
    first_name = person.first_name
    last_name = person.last_name
    print(f"     '{party_id}': ('{first_name}','{last_name}'),")
print("}")
