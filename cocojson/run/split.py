import argparse

from cocojson.tools import split_from_file


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cocojson", help="Path to coco.json to chop up", type=str)
    ap.add_argument(
        "--ratios",
        help="List of ratios to split by",
        type=float,
        required=True,
        nargs="+",
    )
    ap.add_argument(
        "--names",
        help="List of names of the splits. Must be same length as ratios.",
        type=str,
        nargs="+",
    )
    ap.add_argument(
        "--shuffle",
        help="Flag to shuffle images before splitting. Defaults to False.",
        action="store_true",
    )
    args = ap.parse_args()

    split_from_file(
        args.cocojson, args.ratios, names=args.names, do_shuffle=args.shuffle
    )


if __name__ == "__main__":
    main()
