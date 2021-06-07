# Map Categories

Remove images annotated with certain "ignore" category labels. This is usually used for removing rubbish images that are pointed out by annotators to ignore frame.

Default ignore_list = ["ignore"]

"ignore" labels will ignore entire image, take out image and associated annotations. "ignore" labels also taken out from categories

## Usage

```bash
python3 -m cocojson.run.ignore_prune -h
```

```
usage: ignore_prune.py [-h] [--ignore [IGNORE [IGNORE ...]]] [--out OUT] json

positional arguments:
  json                  Path to coco json

optional arguments:
  -h, --help            show this help message and exit
  --ignore [IGNORE [IGNORE ...]]
                        list of ignore labels. Defaults to ["ignore"].
  --out OUT             Output json path
```

## Examples

```bash
python3 -m cocojson.run.ignore_prune /data/cute_kittens_puppies/catdog.json
```

```bash
python3 -m cocojson.run.ignore_prune /data/cute_kittens_puppies/catdog.json --ignore ignore ignore_frame
```
