"""Generate bibliography for search."""

import argparse
import json
from pathlib import Path

import pyalex
from pyalex import Works


# [const]
WIKIDATA_LAND_SNAIL = "https://www.wikidata.org/wiki/Q6484264"
# [/const]


# [main]
def main():
    """Main driver."""
    args = parse_args()
    if args.email:
        pyalex.config.email = args.email
    pager = (
        Works()
        .filter(concepts={"wikidata": args.concept})
        .paginate(method="page", per_page=200)
    )
    counter = 0
    for page in pager:
        for work in page:
            counter += 1
            if args.verbose:
                print(counter)
            ident = work["id"].split("/")[-1]
            data = {
                "doi": work["doi"],
                "year": work["publication_year"],
                "abstract": work["abstract"],
            }
            if all(data.values()):
                Path(args.outdir, f"{ident}.json").write_text(
                    json.dumps(data, ensure_ascii=False)
                )
# [/main]


# [parse_args]
def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--concept", type=str, default=WIKIDATA_LAND_SNAIL, help="Wikidata concept URL"
    )
    parser.add_argument("--email", type=str, default=None, help="user email address")
    parser.add_argument("--outdir", type=str, required=True, help="output directory")
    parser.add_argument(
        "--verbose", action="store_true", default=False, help="report progress"
    )
    return parser.parse_args()
# [/parse_args]


if __name__ == "__main__":
    main()
