import argparse

from cocojson.tools import merge_jsons_files

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir_of_jsons", help="Path to folder of json files to merge")
    args = parser.parse_args()
    merge_jsons_files(args.dir_of_jsons)

if __name__ == "__main__":
    main()
