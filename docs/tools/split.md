# Split Dataset

Split up a COCO JSON file by images into N sets defined by ratio of total images

Optionally, able to give names which corresponds to the ratios

To shuffle images, flag `shuffle=True`.

## Usage

```bash
python3 -m cocojson.run.split -h
```

```
usage: split.py [-h] --ratios RATIOS [RATIOS ...] [--names NAMES [NAMES ...]]
                [--shuffle]
                cocojson

positional arguments:
  cocojson              Path to coco.json to chop up

optional arguments:
  -h, --help            show this help message and exit
  --ratios RATIOS [RATIOS ...]
                        List of ratios to split by
  --names NAMES [NAMES ...]
                        List of names of the splits. Must be same length as
                        ratios.
  --shuffle             Flag to shuffle images before splitting. Defaults to
                        False.
```

## Examples

```bash
python3 -m cocojson.run.split /data/datasetA/all.json --ratio 0.5 0.5  
```

```bash
python3 -m cocojson.run.split /data/datasetA/all.json --ratio 0.8 0.1 0.1  --names train val test 
```

```bash
python3 -m cocojson.run.split /data/datasetA/all.json --ratio 0.8 0.1 0.1 --names train val test --shuffle
```
