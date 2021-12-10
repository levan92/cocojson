import argparse

from cocojson.tools import filter_cat_from_files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json", help="Path to coco json")
    ap.add_argument(
        "--cats", help="Categories to keep, provide list, space separated", nargs="+"
    )
    ap.add_argument(
        "--remove-empty",
        help="Remove (now) empty/negative images (no annotations associated with it)",
        action="store_true",
    )
    ap.add_argument("--out", help="Output json path", type=str)
    args = ap.parse_args()

    filter_cat_from_files(
        args.json, args.cats, out_json=args.out, remove_empty=args.remove_empty
    )


if __name__ == "__main__":
    main()
