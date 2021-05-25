# CVAT Video XML to COCO JSON

Converts CVAT Video XML to COCO JSON while preserving track information.

```bash
python3 -m cocojson.run.cvatvid2coco -h
```

```
usage: cvatvid2coco.py [-h] [--outjson OUTJSON] xml root

positional arguments:
  xml                Path to CVAT Video XML
  root               Path to images root directory

optional arguments:
  -h, --help         show this help message and exit
  --outjson OUTJSON  Path to output json. Defaults to "<task_name>.json"
                     sibling to given root directory.
```

## Examples

```bash
python3 -m cocojson.run.cvatvid2coco /media/dh/HDD/cute_kittens_puppies/cvat_dump/task_catdog-2021_05_25_07_16_22-cvatforvideo1.1/annotations.xml /media/dh/HDD/cute_kittens_puppies/smaller_set
```
