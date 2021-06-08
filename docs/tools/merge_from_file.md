# Merge From File

This is a way of merging datasets (each in coco format) based on a list file.  

`merge_list` is a txt file which contains a list of coco dataset directories to merge. Each coco dataset directory should have an `images` folder and a `<directory name>.json` annotation file. In the source list file, dataset split modes are indicated by [square brackets], followed by the constituent directory names. An empty lines or new square bracket will indicate the end of the previous split. Directory names must be unique.

For e.g.:
```
[train]
iphone_dataset1
iphone_dataset2
dslr_dataset1
# comments
dslr_dataset2

[val]
iphone_dataset3
dslr_dataset3
```

Comments ("#" preceding line) are ignored.

`root` is the parent folder containing all the coco dataset folders (can be nested, but dataset folder names have to be unique). If not given, will search within `merge_list`'s folder.

This will merge all categories in all given datasets.

Merging logic follows the usual [merge](./merge.md).

## Usage

```bash
python3 -m cocojson.run.merge_from_file -h
```

```
usage: merge_from_file.py [-h] [--root ROOT] mergelist output

positional arguments:
  mergelist    Path to merge list
  output       Path to output directory

optional arguments:
  -h, --help   show this help message and exit
  --root ROOT  Path to parent folder containing all the coco dataset folders
               to be merged (optional, will search mergelist directory if not
               given.)
```

## Examples

```bash
python3 -m cocojson.run.merge_from_file /data/datasets_split.txt  /data/test_collated/
```
