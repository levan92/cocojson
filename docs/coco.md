# The COCO JSON Format

```
{
    "info": {
        ...  optional, but some fields good to have
    },
    "licenses": [
        ... optional
    ],
    "categories": [
        ...
    ],
    "images": [
        ...
    ],
    "annotations": [
        ...
    ]
}
```

## Info

```
{
    "info": {
        "year": ...,
        "version": ...,
        "description": ...,
        "contributor": ...,
        "url": ...,
        "date_created": ...
    }
}
```

## Categories

```
{
    "categories":[
        {
            "id": int (usually start from 1),
            "name": category name,
            "supercategory": optional
        },
        ...
    ]
}
```

## Images

```
{
    "images":[
        {
            "id": int (usually start from 1),
            "file_name": subpath that should append to root image directory to give you a path to the image,
            "height": int,
            "width": int,
        },
        ...
    ]
}
```

This should be a complete list of all relevant images (whether positive or negative)

`file_name` has conventionally been a file name, but over here we defined it as a subpath so that we are flexible with the folder organisation structure and naming format within the root image directory.  

## Annotations

Complete list of all relevant images (whether positive or negative)

```
{
    "annotations":[
        {
            "id": int (usually start from 1),
            "image_id": corresponding image id,
            "category_id": corresponding category id, 
            "bbox": [left, top, width, height],
            "area": float,
            "iscrowd": 0 or 1, 
            "attributes": {
                "occluded": bool,
                "track_id": int (usually start from 0),
                "keyframe": bool,
            },
            "segmentation": optional,
        },
        ...
    ]
}
```

### Storing track information

Some annotations are done with tracking/interpolation (for CVAT), COCO JSON format should be able to encode these track information within. Here, we define it inside the `attributes` dict of each `annotation`:

- `track_id` 
- `keyframe`: this is only relevant for CVAT interpolation mode, which tells if this annotation is a keyframe or not (CVAT linearly interpolates boxes between keyframes)

## References

https://cocodataset.org/#format-data

https://www.immersivelimit.com/tutorials/create-coco-annotations-from-scratch/#coco-dataset-format

https://roboflow.com/formats/coco-json
