"""
Insert any extra attributes/image meta information associated with the images into the coco json file.  

Input will be a paired list of image name (comma seperated) and meta-information, together with the attribute name

For example:

    Paired List:
        img1.jpg,iphone
        img2.jpg,iphone
        img3.jpg,dslr
        img4.jpg,dslr

    Attribute name: "source"

Will be inserted into the coco json under each image's "attributes": 

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

If `collate_count` is flagged, image counts of the respective attributes will be given in the "info" block of the coco json under "image_meta_count". 

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

"""
from pathlib import Path
from collections import defaultdict

from cocojson.utils.common import read_coco_json, path, write_json_in_place

IMAGES_ATTRIBUTES = "attributes"
INFO_IMAGEMETACOUNT = "image_meta_count"


def insert_img_meta_from_file(
    coco_json,
    paired_list_file,
    attribute_name="metainfo",
    out_json=None,
    collate_count=False,
):
    coco_dict, setname = read_coco_json(coco_json)
    paired_list = path(paired_list_file)

    img2metainfo = {}
    with paired_list.open("r") as f:
        for line in f.readlines():
            fp, val = line.strip().split(",")
            fn = Path(fp).stem  # just in case full path is given
            img2metainfo[fn] = val

    coco_dict = insert_img_meta(
        coco_dict,
        img2metainfo,
        attribute_name=attribute_name,
        collate_count=collate_count,
    )

    write_json_in_place(coco_json, coco_dict, append_str="inserted", out_json=out_json)


def insert_img_meta(
    coco_dict, img2metainfo, attribute_name="metainfo", collate_count=False
):
    if collate_count:
        count = defaultdict(int)

    for img_block in coco_dict["images"]:
        img_name = img_block["file_name"]
        img_stem = Path(img_name).stem
        assert img_stem in img2metainfo, img_name
        val = img2metainfo[img_stem]
        if IMAGES_ATTRIBUTES not in img_block:
            img_block[IMAGES_ATTRIBUTES] = {}
        img_block[IMAGES_ATTRIBUTES][f"{attribute_name}"] = val
        if collate_count:
            count[val] += 1

    if collate_count:
        if INFO_IMAGEMETACOUNT not in coco_dict["info"]:
            coco_dict["info"][INFO_IMAGEMETACOUNT] = {}
        coco_dict["info"][INFO_IMAGEMETACOUNT][f"{attribute_name}"] = count

    return coco_dict
