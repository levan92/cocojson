import argparse

from cocojson.tools import sample


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json", help="Path to coco json")
    ap.add_argument("imgroot", help="Path to img root")
    ap.add_argument("outdir", help="Path to output dir")
    ap.add_argument("--k", help="Random k images to extract", type=int, default=10)
    args = ap.parse_args()

    sample(args.json, args.imgroot, args.outdir, k=args.k)


if __name__ == "__main__":
    main()
