# Insert Images Meta-Information

Insert any extra attributes/image meta information associated with the images into the coco json file.  

Input will be a paired list of image name (comma seperated) and meta-information, together with the attribute name

For example:

    Paired List:
        ```
        img1.jpg,iphone
        img2.jpg,iphone
        img3.jpg,dslr
        img4.jpg,dslr
        ```

    Attribute name: "source"

Will be inserted into the coco json under each image's "attributes":

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

If `collate_count` is flagged, image counts of the respective attributes will be given in the "info" block of the coco json under "image_meta_count".

```
{
    "info": {
        "year": ...,
        "version": ...,
        "description": ...,
        "contributor": ...,
        "url": ...,
        "date_created": ...,
        "image_meta_count": (this is an addition specific to this repo) dictionaries of image meta information  
    }
}
```

## Usage

```bash
python3 -m cocojson.run.insert_img_meta -h
```

```
usage: insert_img_meta.py [-h] [--attribute ATTRIBUTE] [--out OUT]
                          [--collate-count]
                          json pairedlist

positional arguments:
  json                  Path to coco json
  pairedlist            Path to paired list of img name to meta info

optional arguments:
  -h, --help            show this help message and exit
  --attribute ATTRIBUTE
                        Name of meta info/attribute. Defaults to metainfo.
  --out OUT             Output json path
  --collate-count       Flag to collate meta-info counts in coco info section
```

## Examples

```bash
python3 -m cocojson.run.insert_img_meta /data/coco.json /data/img2source.list --attribute source
```

```bash
python3 -m cocojson.run.insert_img_meta /data/coco.json /data/img2source.list --attribute source --collate-count
```
