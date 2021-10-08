import argparse

from cocojson.tools import viz


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json", help="Path to coco json")
    ap.add_argument("imgroot", help="Path to img root")
    ap.add_argument(
        "--outdir",
        help="Path to output dir, leave out to not write out",
        type=str,
        nargs="?",
        const=True,
    )
    ap.add_argument(
        "--sample",
        help="Num of imgs to sample, leave this flag out to process all.",
        type=int,
    )
    ap.add_argument("--show", help="To imshow", action="store_true")
    args = ap.parse_args()

    viz(
        args.json,
        args.imgroot,
        outdir=args.outdir,
        sample_k=args.sample,
        show=args.show,
    )


if __name__ == "__main__":
    main()
