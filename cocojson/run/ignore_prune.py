import argparse

from cocojson.tools import ignore_prune_from_file

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('json', help='Path to coco json')
    ap.add_argument('--ignore', help='list of ignore labels. Defaults to ["ignore"].', nargs='*', default=['ignore'])
    ap.add_argument('--out', help='Output json path', type=str)
    args = ap.parse_args()

    ignore_prune_from_file(args.json, ignore_list=args.ignore, out_json=args.out)

if __name__ == '__main__':
    main()