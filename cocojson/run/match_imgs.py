import argparse

from cocojson.tools import match_imgs_from_file


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cocojsonA", help="Path to reference coco json")
    ap.add_argument("cocojsonB", help="Path to coco json to be trimmed")
    ap.add_argument("--outjson", help="Path to output json (optional)")
    args = ap.parse_args()

    match_imgs_from_file(args.cocojsonA, args.cocojsonB, outjson=args.outjson)


if __name__ == "__main__":
    main()
