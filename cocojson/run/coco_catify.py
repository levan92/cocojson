import argparse

from cocojson.tools import coco_catify_from_files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json", help="Path to coco json")
    ap.add_argument("map_json", help="Path to mapping json")
    ap.add_argument(
        "--new-json",
        help="Optional to provide 'coco categories'. Will default to coco 80 classes.",
    )
    ap.add_argument("--out", help="Output json path", type=str)
    ap.add_argument(
        "--map-is-id",
        help="Flag to indicate that mapping given is in cat ids instead of cat names.",
        action="store_true",
    )
    args = ap.parse_args()

    coco_catify_from_files(
        args.json,
        args.map_json,
        args.new_json,
        out_json=args.out,
        map_is_id=args.map_is_id,
    )


if __name__ == "__main__":
    main()
