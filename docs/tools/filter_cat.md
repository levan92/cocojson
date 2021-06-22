# Filter Categories

Filter categories from COCO JSON.

Takes in a list of category names to keep.

## Usage

```bash
python3 -m cocojson.run.filter_cat -h
```

```
usage: filter_cat.py [-h] [--cats CATS [CATS ...]] [--out OUT] json

positional arguments:
  json                  Path to coco json

optional arguments:
  -h, --help            show this help message and exit
  --cats CATS [CATS ...]
                        Categories to keep, provide list, space separated
  --out OUT             Output json path
```

## Examples

```bash
python3 -m cocojson.run.filter_cat test_datasets/merged/merged.json --cats apple person```
