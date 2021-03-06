# Merge

Merges multiple datasets in coco json format

Expected format of 1 x Dataset:
- 1 x json file 
- 1 x Image Folder (to get to the image, path is assumed to be "Image Folder"/"file_name" given in json)

Merged Dataset:
- 1 x json file (image's "file_name" will be subpaths, for eg, "Image Folder from DatasetA/image01.png")
- Master Images Folder 
    - Image Folder from DatasetA
    - Image Folder from DatasetA
    - ...

Only given category IDs for each dataset will be merged. Merged category list will merge constituent categories based on category name. If no `-c` is flagged, default will take all categories to merge.

See also [Merge From File](./merge_from_file.md).

## Usage

```bash
python3 -m cocojson.run.merge -h
```

```
usage: merge.py [-h] -j JSON -r ROOT [-c CIDS [CIDS ...]] -o OUTPUT
                [--outname OUTNAME]

optional arguments:
  -h, --help            show this help message and exit
  -j JSON, --json JSON  path to coco json
  -r ROOT, --root ROOT  path to root image directory
  -c CIDS [CIDS ...], --cids CIDS [CIDS ...]
                        category ids to merge (optional, default will take all
                        categories to merge.)
  -o OUTPUT, --output OUTPUT
                        path to output directory
  --outname OUTNAME     name of output json (default: "merged")

Typical usage: merge_coco.py \ 
-j <path_to_coco_json_1> -r <path_to_images_1>  -c 1 \ 
-j <path_to_coco_json_2> -r <path_to_images_2> -c 1 2 \ 
-j <path_to_coco_json_3> -r <path_to_images_3> -c 1 2 \ 
-o <path_to_output_dataset>
Categories will be merged by category name
```

## Examples

```bash
python3 -m cocojson.run.merge -r test_datasets/datasetA/images/ -j test_datasets/datasetA/val.json -c 1 -r test_datasets/datasetB/images/ -j test_datasets/datasetB/val.json -c 1 -r test_datasets/datasetC/images/ -j test_datasets/datasetC/val.json -c 2 -r test_datasets/datasetD/images/ -j test_datasets/datasetD/val.json -c 3 -o test_datasets/merged/
```

```bash
python3 -m cocojson.run.merge -r /home/dh/Workspace/cocojson/test_datasets/datasetA/images -j /home/dh/Workspace/cocojson/test_datasets/datasetA/val.json  -r test_datasets/datasetC/images/ -j test_datasets/datasetC/val.json  -o test_datasets/merged/
```
