import argparse
import json
from pathlib import Path

from electos.datamodels.nist.indexes import ElementIndex
from electos.datamodels.nist.models.edf import ElectionReport

from electos.ballotmaker.data.extractor import (
    ballot_style_external_id,
    extract_ballot_styles,
    extract_contests,
)


def report(root, index, nth, **opts):
    """Generate data needed by BallotLab."""
    ballot_styles = list(extract_ballot_styles(root, index))
    if not (1 <= nth <= len(ballot_styles)):
        print(f"Ballot styles: {nth} is out of range [1-{len(ballot_styles)}]")
        return
    ballot_style = ballot_styles[nth - 1]
    data = {}
    id_ = ballot_style_external_id(ballot_style)
    data["ballot_style"] = id_
    contests = list(extract_contests(ballot_style, index))
    if not contests:
        print(f"No contests found for ballot style: {id_}\n")
    data["contests"] = contests
    print(json.dumps(data, indent = 4))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file", type = Path,
        help = "Test case data (JSON)"
    )
    parser.add_argument(
        "nth", nargs = "?", type = int, default = 1,
        help = "Index of the ballot style, starting from 1 (default: 1)"
    )
    parser.add_argument(
        "--debug", action = "store_true",
        help = "Enable debugging output and stack traces"
    )
    opts = parser.parse_args()
    file = opts.file
    opts = vars(opts)

    try:
        with file.open() as input:
            text = input.read()
            data = json.loads(text)
        edf = ElectionReport(**data)
        index = ElementIndex(edf, "ElectionResults")
        report(edf, index, **opts)
    except Exception as ex:
        if opts["debug"]:
            raise ex
        print("error:", ex)


if __name__ == '__main__':
    main()
