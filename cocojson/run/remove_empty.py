import argparse

from cocojson.tools import remove_empty_from_files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json", help="Path to coco json")
    ap.add_argument("--out", help="Output json path", type=str)
    args = ap.parse_args()

    remove_empty_from_files(args.json, out_json=args.out)


if __name__ == "__main__":
    main()
