import argparse
import json
from dataclasses import asdict
from pathlib import Path

from electos.ballotmaker.data.extractor import extract_ballot_data


def report(data, **opts):
    """Generate data needed by BallotLab."""
    ballot_data = extract_ballot_data(data)
    ballot_data = [asdict(_) for _ in ballot_data]
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
