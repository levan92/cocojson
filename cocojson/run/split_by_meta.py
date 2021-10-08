import argparse

from cocojson.tools import split_by_meta_from_file


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cocojson", help="Path to coco.json to chop up", type=str)
    ap.add_argument("attribute", help="Image meta information attribute name", type=str)
    ap.add_argument(
        "--preserve-img-id", help="Flag to preserve image ids", action="store_true"
    )
    args = ap.parse_args()

    split_by_meta_from_file(
        args.cocojson, args.attribute, preserve_img_id=args.preserve_img_id
    )


if __name__ == "__main__":
    main()
