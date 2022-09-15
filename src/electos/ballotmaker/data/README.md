Data to use for BallotLab inputs. The data is extracted from EDF test cases
and constrained to the data model Ballot Lab is using.

Output file naming format is `{test-case-source}_{ballot-style-id}.json`.
Note the use of `-` to separate words, and `_` to separate the name parts.

All the current examples are taken from these EDF files:

- https://github.com/TrustTheVote-Project/NIST-1500-100-103-examples/blob/main/test_cases/june_test_case.json

To run it:

- Install the BallotLab fork and change to the 'edf-data-to-ballot' branch.

      git clone https://github.com/ion-oset/BallotLab -b edf-data-to-ballot

- Install the project dependencies:

      poetry install

- Run:

      python scripts/ballot-lab-data.py <test-case-file> <index of ballot style>

  e.g.

      python scripts/ballot-lab-data.py june_test_case.json 1

Structure of output:

- Output is a series of contests, grouped by contest type (candidate, ballot
  measure)
- Within a contest type order of records is preserved.
- The `VotingVariation` in the EDF is `vote_type` here. It can be filtered.
  - `vote_type` of `plurality` is the simplest kind of ballot.
  - Ignore `n-of-m` and `ranked-choice` until later.
- Write-ins are integrated into the candidate list.
- The fields were selected to match what is needed for `plurality` candidate
  contests and a little extra.
  - To add fields or modify them we should modify `extract_{contest type}_contest`.

Notes:

- There are no `Header`s or `OrderedHeader`s in `june_test_case.json`.
