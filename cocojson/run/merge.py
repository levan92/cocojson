import argparse

from cocojson.tools import merge

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Typical usage: merge_coco.py \ \n' +
               '-j <path_to_coco_json_1> -r <path_to_images_1>  -c 1 \ \n' +
               '-j <path_to_coco_json_2> -r <path_to_images_2> -c 1 2 \ \n' +
               '-j <path_to_coco_json_3> -r <path_to_images_3> -c 1 2 \ \n' +
               '-o <path_to_output_dataset>\n' + 
               'Categories will be merged by category name'
    )
    parser.add_argument('-j', '--json', help='path to coco json', action='append', required=True)
    parser.add_argument('-r', '--root', help='path to root image directory', action='append', required=True)
    parser.add_argument('-c', '--cids', help='category ids to merge', action='append', nargs='+', required=True, type=int)
    parser.add_argument('-o', '--output', help='path to output directory', required=True)
    parser.add_argument('--outname', help='name of output json (default: "merged")', default='merged')
    args = parser.parse_args()

    merge(args.json, args.root, args.cids, args.output, outname=args.outname)

if __name__ == '__main__':
    main()