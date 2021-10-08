# Split by Image Meta-Information

Split up a COCO JSON file by image meta information/attributes

```
{
    "images":[
        {
            "id": int (usually start from 1),
            "file_name": subpath that should append to root image directory to give you a path to the image,
            "height": int,
            "width": int,
            "attributes": {
                "attribute name": any extra meta info associated with image,
            },

        },
        ...
    ]
}
```

`meta_keys_list` is a list of keys to a nested dictionary. For e.g., in the above case, it will be `["attributes", "attribute name"]`

For `cocojson.run.split_by_meta`, the `attribute` argument refer to the chosen key within the "attributes" dictionary.  

If attribute is not present for any of the image, it will be split to "nil".

Flag `perserve_img_id` in order to preserve original image IDs in the new jsons. 

## Usage

```bash
python3 -m cocojson.run.split_by_meta -h
```

```
usage: split_by_meta.py [-h] cocojson attribute

positional arguments:
  cocojson    Path to coco.json to chop up
  attribute   Image meta information attribute name

optional arguments:
  -h, --help  show this help message and exit
  --preserve-img-id  Flag to preserve image ids 
```

## Examples

```bash
python3 -m cocojson.run.split_by_meta /data/coco.json source
```
