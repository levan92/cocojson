# Map Categories

Mapping categories to a new dataset. Usually used for converting annotation labels to actual class label for training.

- New categories are defined in a json file in coco format
- Mapping is also defined in another json file, a dict of old label names to new label names. Multiple old label names can map to same new label name.

    For example:
    '''json
       {
            "child": "human",
            "adult": "human",
            "chihuahua" : "dog",
            "bulldog": "dog",
        }
    '''

- By default, any old label names not given in mapping will be taken out in the new dataset along with associated annotations. To preserve old label names in the new dataset, please flag `keep_old`. 

```bash
python3 -m cocojson.run.map_cat -h
```

```
usage: map_cat.py [-h] [--out OUT] [--keep-old] json new_json map_json

positional arguments:
  json        Path to coco json
  new_json    Path to new categories json
  map_json    Path to mapping json

optional arguments:
  -h, --help  show this help message and exit
  --out OUT   Output json path
  --keep-old  Flag to keep old categories not mentioned in mapping
```

## Examples

```bash
python3 -m cocojson.run.map_cat /data/kitty_pups/catdog.json /data/kitty_pups/new_cats.json /data/kitty_pups/map.json
```

```bash
python3 -m cocojson.run.map_cat /data/kitty_pups/catdog.json /data/kitty_pups/new_cats.json /data/kitty_pups/map.json --keep-old    
```
