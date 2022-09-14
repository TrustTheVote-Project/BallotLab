import argparse
import json
from pathlib import Path

from electos.datamodels.nist.indexes import ElementIndex
from electos.datamodels.nist.models.edf import ElectionReport

from electos.ballotmaker.data.extractor import extract_ballot_data


def report(data, **opts):
    """Generate data needed by BallotLab."""
    document = ElectionReport(**data)
    index = ElementIndex(document, "ElectionResults")
    ballot_data = extract_ballot_data(document, index)
    print(json.dumps(ballot_data, indent = 4))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file", type = Path,
        help = "Test case data (JSON)"
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
        report(data, **opts)
    except Exception as ex:
        if opts["debug"]:
            raise ex
        print("error:", ex)


if __name__ == '__main__':
    main()
