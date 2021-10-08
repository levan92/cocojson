import argparse

from cocojson.tools import ignore_prune_from_file


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json", help="Path to coco json")
    ap.add_argument(
        "--ignore",
        help='list of ignore labels. Defaults to ["ignore"].',
        nargs="*",
        default=["ignore"],
    )
    ap.add_argument("--out", help="Output json path", type=str)
    ap.add_argument(
        "--img-root",
        help="Image root to prune ignored images from. Optional. If given, it will prune images. Else, it will not.",
        type=str,
    )
    args = ap.parse_args()

    ignore_prune_from_file(
        args.json, ignore_list=args.ignore, out_json=args.out, img_root=args.img_root
    )


if __name__ == "__main__":
    main()
