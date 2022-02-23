# COCO Categori-fy

Convert your custom dataset into COCO categories. Usually used for testing a coco-pretrained model against a custom dataset with overlapping categories with the [80 COCO classes](https://github.com/levan92/coco-classes-mapping/blob/master/coco80.names)

Define mapping (old to new, new being coco classes): 
    Either in Category names, for e.g.:
        {
            "human": "person",
            "ship": "boat"
        }
    or in Category ID (you will need to flag `map_is_id`), for e.g.:
        {
            "1": 1,
            "2": 9
        }

Note: Annotations with original categories not in the mapping json will be removed.  

## Usage

```bash
python3 -m cocojson.run.coco_catify -h
```

```
usage: coco_catify.py [-h] [--new-json NEW_JSON] [--out OUT] [--map-is-id]
                      json map_json

positional arguments:
  json                 Path to coco json
  map_json             Path to mapping json

optional arguments:
  -h, --help           show this help message and exit
  --new-json NEW_JSON  Optional to provide 'coco categories'. Will default to
                       coco 80 classes.
  --out OUT            Output json path
  --map-is-id          Flag to indicate that mapping given is in cat ids
                       instead of cat names.
```

## Examples

```bash
python3 -m cocojson.run.coco_catify /data/kitty_pups/catdog.json /data/kitty_pups/map.json
```

```bash
python3 -m cocojson.run.coco_catify /data/kitty_pups/catdog.json /data/kitty_pups/map_id.json --map-is-id
```

```bash
python3 -m cocojson.run.coco_catify /data/kitty_pups/catdog.json /data/kitty_pups/map.json --new-json /data/coco/coco_categories.json
```
