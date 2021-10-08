import argparse

from cocojson.convert.crowdhuman2coco import convert


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("odgt", help="Path to CrowdHuman odgt file")
    ap.add_argument("root", help="Path to images root directory")
    ap.add_argument(
        "--outjson",
        help='Path to output json. Defaults to "<task_name>.json" sibling to given root directory.',
    )
    args = ap.parse_args()

    convert(args.odgt, args.root, outjson=args.outjson)


if __name__ == "__main__":
    main()
