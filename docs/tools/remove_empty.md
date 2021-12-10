# Remove Empty

Remove empty/negative images from COCO JSON, aka images without associated annotations.

Original image IDs are preserved. 

## Usage

```bash
python3 -m cocojson.run.remove_empty -h
```

```
usage: remove_empty.py [-h] [--out OUT] json

positional arguments:
  json        Path to coco json

optional arguments:
  -h, --help  show this help message and exit
  --out OUT   Output json path
```

## Examples

```bash
python -m cocojson.run.remove_empty val
_withempty.json
```
