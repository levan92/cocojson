import argparse

from cocojson.convert.log2coco import convert


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log_annot", help="Path to log annotation file")
    ap.add_argument("root", help="Path to images root directory")
    ap.add_argument(
        "--outjson",
        help='Path to output json. Defaults to "<task_name>.json" sibling to given root directory.',
    )
    args = ap.parse_args()

    convert(args.log_annot, args.root, outjson=args.outjson)


if __name__ == "__main__":
    main()
