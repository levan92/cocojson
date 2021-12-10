# Filter Categories

Filter categories from COCO JSON.

Takes in a list of category names or list of category ids to keep.

All images are kept by default (meaning there is a possibility of negative images with no annotations). To remove them as well, flag `--remove-empty`.

Note: Image IDs and Annotation IDs are preserved from original, but new categories have their IDs "reset" to 1.  

## Usage

```bash
python3 -m cocojson.run.filter_cat -h
```

```
usage: filter_cat.py [-h] [--cats CATS [CATS ...]] [--remove-empty] [--out OUT] json

positional arguments:
  json                  Path to coco json

optional arguments:
  -h, --help            show this help message and exit
  --cats CATS [CATS ...]
                        Categories to keep, provide list, space separated
  --remove-empty        Remove (now) empty/negative images (no annotations associated with it)
  --out OUT             Output json path
```

## Examples

```bash
python3 -m cocojson.run.filter_cat test_datasets/merged/merged.json --cats apple person
```
