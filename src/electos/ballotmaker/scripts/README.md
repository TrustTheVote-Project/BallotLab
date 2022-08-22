Extract data from NIST EDF models for use by BallotLab.

## Requirements

- The script requires `nist-datamodels`,  using a version that has element indexes.

## Inputs

Filenames are of the format `{test-case-source}_{ballot-style-id}.json`.
Note the use of `-` to separate words, and `_` to separate the name parts.

Inputs are EDF JSON files. Get them from:

- https://github.com/TrustTheVote-Project/NIST-1500-100-103-examples/blob/main/test_cases/

The script is `ballot-lab-data.py`. It takes an EDF test case, and the index of
the ballot style to use (a number from 1 to N, that defaults to 1.).

To run it:

- Install `nist-datamodels`, using a version that has element indexes.
- Run:

      python ballot-lab-data.py <test-case-file> [<index of ballot style>]

  e.g.

      python ballot-lab-data.py june_test_case.json 1

## Outputs

- Output is JSON files with contests, grouped by contest type.
- The `VotingVariation` in the EDF is `vote_type` here.
- Write-ins don't affect the candidate list. They are returned as a count.
  Presumably they would all be the same and all that's needed is their number.
  They can be ignored.`
- The fields were selected to match what is needed for `plurality` candidate
  contests and a little extra. We can add other `VoteVariation`s and ballot
  measure contests as needed.

## Complications

- There are no `Header`s or `OrderedHeader`s in the test cases.
