import argparse

from cocojson.tools import map_cat_from_files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json", help="Path to coco json")
    ap.add_argument("new_json", help="Path to new categories json")
    ap.add_argument("map_json", help="Path to mapping json")
    ap.add_argument("--out", help="Output json path", type=str)
    ap.add_argument(
        "--keep-old",
        help="Flag to keep old categories not mentioned in mapping",
        action="store_true",
    )
    ap.add_argument(
        "--map-is-id",
        help="Flag to indicate that mapping given is in cat ids instead of cat names.",
        action="store_true",
    )
    args = ap.parse_args()

    map_cat_from_files(
        args.json,
        args.new_json,
        args.map_json,
        out_json=args.out,
        keep_old=args.keep_old,
        map_is_id=args.map_is_id,
    )


if __name__ == "__main__":
    main()
