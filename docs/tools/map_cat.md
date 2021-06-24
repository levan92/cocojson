# Map Categories

Mapping categories to a new dataset. Usually used for converting annotation labels to actual class label for training.
- New categories are defined in a json file in coco format
- Mapping is also defined in another json file, a dict of old label names to new label names. Multiple old label names can map to same new label name.
    Either in Category Names, for e.g.:
       {
            "child": "human",
            "adult": "human",
            "chihuahua" : "dog",
            "bulldog": "dog",
        }
    Or in Category ID (You will need to flag `map_is_id`), for e.g.:
    {
        "1":1,
        "2":1,
        "3":2,
        "4":2
    }

- By default, any old label names not given in mapping will be taken out in the new dataset along with associated annotations. To preserve old label names in the new dataset, please flag `keep_old`.

## Usage

```bash
python3 -m cocojson.run.map_cat -h
```

```
usage: map_cat.py [-h] [--out OUT] [--keep-old] [--map-is-id]
                  json new_json map_json

positional arguments:
  json         Path to coco json
  new_json     Path to new categories json
  map_json     Path to mapping json

optional arguments:
  -h, --help   show this help message and exit
  --out OUT    Output json path
  --keep-old   Flag to keep old categories not mentioned in mapping
  --map-is-id  Flag to indicate that mapping given is in cat ids instead of
               cat names.
```

## Examples

```bash
python3 -m cocojson.run.map_cat /data/kitty_pups/catdog.json /data/kitty_pups/new_cats.json /data/kitty_pups/map.json
```

```bash
python3 -m cocojson.run.map_cat /data/kitty_pups/catdog.json /data/kitty_pups/new_cats.json /data/kitty_pups/map.json --keep-old    
```

```bash
python3 -m cocojson.run.map_cat /data/kitty_pups/catdog.json /data/kitty_pups/new_cats.json /data/kitty_pups/map_id.json  --map-is-id
```