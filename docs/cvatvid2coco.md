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
python3 -m cocojson.run.cvatvid2coco /data/kitty_pups/cvat_dump/task_cvatforvideo/annotations.xml /data/kitty_pups/smaller_set
```
