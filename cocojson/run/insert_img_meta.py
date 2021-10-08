import argparse

from cocojson.tools import insert_img_meta_from_file


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json", help="Path to coco json")
    ap.add_argument("pairedlist", help="Path to paired list of img name to meta info")
    ap.add_argument(
        "--attribute",
        help="Name of meta info/attribute. Defaults to metainfo.",
        default="metainfo",
    )
    ap.add_argument("--out", help="Output json path", type=str)
    ap.add_argument(
        "--collate-count",
        help="Flag to collate meta-info counts in coco info section",
        action="store_true",
    )
    args = ap.parse_args()

    insert_img_meta_from_file(
        args.json,
        args.pairedlist,
        attribute_name=args.attribute,
        out_json=args.out,
        collate_count=args.collate_count,
    )


if __name__ == "__main__":
    main()
