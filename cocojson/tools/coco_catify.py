"""
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
"""

from cocojson.utils.coco_categories import COCO_CATEGORIES
from cocojson.utils.common import read_coco_json, read_json, write_json_in_place


def coco_catify_from_files(
    coco_json,
    mapping_json,
    new_cat_json=None,
    out_json=None,
    map_is_id=False,
):
    coco_dict, _ = read_coco_json(coco_json)
    mapping_dict = read_json(mapping_json)
    if new_cat_json:
        new_cat_dict = read_json(new_cat_json)
    else:
        new_cat_dict = None

    out_dict = coco_catify(
        coco_dict, mapping_dict, new_categories=new_cat_dict, map_is_id=map_is_id
    )

    write_json_in_place(
        coco_json, out_dict, append_str="coco-catified", out_json=out_json
    )


def coco_catify(coco_dict, mapping_dict, new_categories=None, map_is_id=False):
    if new_categories is None:
        new_categories = COCO_CATEGORIES
    if isinstance(new_categories, dict):
        new_categories = new_categories["categories"]
    assert isinstance(new_categories, list)

    if not map_is_id:
        old_name2id = {}
        for cat in coco_dict["categories"]:
            if cat["name"] in mapping_dict.keys():
                old_name2id[cat["name"]] = cat["id"]
        new_name2id = {}
        for cat in new_categories:
            if cat["name"] in mapping_dict.values():
                new_name2id[cat["name"]] = cat["id"]
        mapping_dict = {old_name2id[k]: new_name2id[v] for k, v in mapping_dict.items()}
    else:
        mapping_dict = {int(k): int(v) for k, v in mapping_dict.items()}

    coco_dict["categories"] = new_categories

    new_annots = []
    for annot in coco_dict["annotations"]:
        if annot["category_id"] in mapping_dict:
            annot["category_id"] = mapping_dict[annot["category_id"]]
            new_annots.append(annot)

    coco_dict["annotations"] = new_annots

    return coco_dict
