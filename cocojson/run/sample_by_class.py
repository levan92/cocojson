import argparse

from cocojson.tools import sample_by_class


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json", help="Path to coco json")
    ap.add_argument("imgroot", help="Path to img root")
    ap.add_argument("outdir", help="Path to output dir")
    ap.add_argument(
        "--class-ks",
        help="How many to sample for each category, can either be single int or a list of int corresponding to each category. Defaults to 10 per category.",
        type=int,
        nargs="*",
        default=10,
    )
    ap.add_argument(
        "--max-img",
        help="Max num of images to be sampled, will retry until it falls below. Defaults to no max limit.",
        type=int,
    )
    ap.add_argument(
        "--retries",
        help="Max number of retries. Defaults to 1000.",
        type=int,
        default=1000,
    )
    args = ap.parse_args()

    sample_by_class(
        args.json,
        args.imgroot,
        args.outdir,
        class_ks=args.class_ks,
        max_img=args.max_img,
        retries=args.retries,
    )


if __name__ == "__main__":
    main()
