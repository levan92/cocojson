"""
Split up a COCO JSON file by image meta information/attributes

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

`meta_keys_list` is a list of keys to a nested dictionary. For e.g., in the above case, it will be `["attributes", "attribute name"]`

For `cocojson.run.split_by_meta`, the `attribute` argument refer to the chosen key within the "attributes" dictionary.  

If attribute is not present for any of the image, it will be split to "nil". 

Flag `perserve_img_id` in order to preserve original image IDs in the new jsons. 

"""
from pathlib import Path
from collections import defaultdict
from copy import deepcopy

from cocojson.utils.common import read_coco_json, dict_val_from_keys_list, write_json


def split_by_meta_from_file(cocojson, meta_attr_name, preserve_img_id=False):
    coco_dict, setname = read_coco_json(cocojson)
    meta_keys_list = ["attributes"]
    meta_keys_list.append(meta_attr_name)
    split_coco_dicts = split_by_meta(
        coco_dict, meta_keys_list, preserve_img_id=preserve_img_id
    )

    cocojson = Path(cocojson)
    for attr, new_cocodict in split_coco_dicts.items():
        json_out = cocojson.parent / f"{cocojson.stem}_{attr}.json"
        write_json(json_out, new_cocodict)


def default_coco_dict():
    new_dict = {
        "images": [],
        "annotations": [],
    }
    return new_dict


def split_by_meta(coco_dict, meta_keys_list, setname="", preserve_img_id=False):
    split_coco_dicts = defaultdict(default_coco_dict)

    img_ids_maps = defaultdict(dict)
    oldimgids2attr = {}
    for img_dict in coco_dict["images"]:
        try:
            attr = dict_val_from_keys_list(img_dict, meta_keys_list)
        except KeyError:
            print("Key error")
            attr = "nil"
        oldimgids2attr[img_dict["id"]] = attr
        new_img_dict = deepcopy(img_dict)
        if preserve_img_id:
            new_img_id = img_dict["id"]
        else:
            new_img_id = len(split_coco_dicts[attr]["images"]) + 1
        img_ids_maps[attr][img_dict["id"]] = new_img_id
        new_img_dict["id"] = new_img_id
        split_coco_dicts[attr]["images"].append(new_img_dict)

    for annot_dict in coco_dict["annotations"]:
        attr = oldimgids2attr[annot_dict["image_id"]]
        new_annot_dict = deepcopy(annot_dict)
        new_annot_dict["id"] = len(split_coco_dicts[attr]["annotations"]) + 1
        new_annot_dict["image_id"] = img_ids_maps[attr][annot_dict["image_id"]]
        split_coco_dicts[attr]["annotations"].append(new_annot_dict)

    for attr, dic in split_coco_dicts.items():
        print(attr)
        if "info" in coco_dict:
            dic["info"] = deepcopy(coco_dict["info"])
            dic["info"]["description"] = f"{attr} only {setname}"
        if "licenses" in coco_dict:
            dic["licenses"] = deepcopy(coco_dict["licenses"])
        if "categories" in coco_dict:
            dic["categories"] = deepcopy(coco_dict["categories"])

    return split_coco_dicts
