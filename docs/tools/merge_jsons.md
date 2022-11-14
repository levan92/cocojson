# Merge JSONs

Merge multiple coco jsons. Assumes image ids are unique across multiple jsons and will also preserve image ids when merging

For example, for merging json files provided by https://www.sama.com/sama-coco-dataset/.

## Usage 

```bash
python3 -m cocojson.run.merge_jsons -h 
``` 

```
usage: merge_jsons.py [-h] dir_of_jsons

positional arguments:
  dir_of_jsons  Path to folder of json files to merge

optional arguments:
  -h, --help    show this help message and exit
```

## Examples 

```bash
python3 -m cocojson.run.merge_jsons /path/to/dir/of/jsons/
```