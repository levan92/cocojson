# Extract only Annotations

Get annotations/predictions only from a COCO JSON. Usually used to generate a list of predictions for COCO evaluation.

if `add_score` is None (default), no score is added to annotation. Else, `add_score` should be a float, in which the score will be added to each annotation. 

## Usage

```bash
python3 -m cocojson.run.pred_only -h
```

```
usage: pred_only.py [-h] [--score SCORE] json

positional arguments:
  json           Path to coco json

optional arguments:
  -h, --help     show this help message and exit
  --score SCORE  Prediction score to be added to all annotations (defaults to
                 None, aka not added).
```

## Examples

```bash
python3 -m cocojson.run.pred_only /data/coco.json
```

```bash
python3 -m cocojson.run.pred_only /data/coco.json --score 1.0
```
