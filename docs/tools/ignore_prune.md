# Map Categories

Remove images annotated with certain "ignore" category labels. This is usually used for removing rubbish images that are pointed out by annotators to ignore frame.

Default ignore_list = ["ignore"]

"ignore" labels will ignore entire image, take out image and associated annotations. "ignore" labels also taken out from categories

If img_root is given, ignored images will be deleted from the img_root. By default when img_root is not given, nothing will happen to the actual ignored image files, just taken out from the coco json.


## Usage

```bash
python3 -m cocojson.run.ignore_prune -h
```

```
usage: ignore_prune.py [-h] [--ignore [IGNORE [IGNORE ...]]] [--out OUT]
                       [--img-root IMG_ROOT]
                       json

positional arguments:
  json                  Path to coco json

optional arguments:
  -h, --help            show this help message and exit
  --ignore [IGNORE [IGNORE ...]]
                        list of ignore labels. Defaults to ["ignore"].
  --out OUT             Output json path
  --img-root IMG_ROOT   Image root to prune ignored images from. Optional. If
                        given, it will prune images. Else, it will not.
```

## Examples

```bash
python3 -m cocojson.run.ignore_prune /data/cute_kittens_puppies/catdog.json
```

```bash
python3 -m cocojson.run.ignore_prune /data/cute_kittens_puppies/catdog.json --ignore ignore ignore_frame
```

```bash
python3 -m cocojson.run.ignore_prune /data/cute_kittens_puppies/catdog.json --ignore ignore ignore_frame --img-root /data/cute_kittens_puppies/images/
```
