# Match Images between 2 COCO JSONs

Match images between COCO JSON A and COCO JSON B. Any images in JSON B that is not found in JSON A will be removed (along with associated annotations)

Match will be through image `file_name`.

## Usage

```bash
python3 -m cocojson.run.match_imgs -h
```

```
usage: match_imgs.py [-h] [--outjson OUTJSON] cocojsonA cocojsonB

positional arguments:
  cocojsonA          Path to reference coco json
  cocojsonB          Path to coco json to be trimmed

optional arguments:
  -h, --help         show this help message and exit
  --outjson OUTJSON  Path to output json (optional)
```

## Examples

```bash
python3 -m cocojson.run.match_imgs /data/cocoA.json /data/cocoB.json
```
