import argparse

from cocojson.tools import pred_only


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json", help="Path to coco json")
    ap.add_argument(
        "--score",
        help="Prediction score to be added to all annotations (defaults to None, aka not added).",
        type=float,
    )
    args = ap.parse_args()

    pred_only(args.json, add_score=args.score)


if __name__ == "__main__":
    main()
