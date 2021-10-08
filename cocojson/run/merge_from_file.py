import argparse

from cocojson.tools import merge_from_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mergelist", help="Path to merge list")
    parser.add_argument("output", help="Path to output directory")
    parser.add_argument(
        "--root",
        help="Path to parent folder containing all the coco dataset folders to be merged (optional, will search mergelist directory if not given.)",
    )
    args = parser.parse_args()

    merge_from_file(args.mergelist, args.output, root=args.root)


if __name__ == "__main__":
    main()
