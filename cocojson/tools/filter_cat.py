"""
Filter categories from COCO JSON.

Takes in a list of category names to keep.
"""
from cocojson.utils.common import read_coco_json, write_json_in_place
from .map_cat import map_cat


def filter_cat_from_files(coco_json, cats_to_keep, out_json=None):
    coco_dict, _ = read_coco_json(coco_json)
    out_dict = filter_cat(coco_dict, cats_to_keep)
    write_json_in_place(coco_json, out_dict, append_str="filtered", out_json=out_json)


def filter_cat(coco_dict, cats_to_keep):
    assert isinstance(cats_to_keep, list), cats_to_keep
    try:
        cats_to_keep = list(map(int, cats_to_keep))
    except:
        print("List doesn't contain ints, moving on.")
    typecheck = type(cats_to_keep[0])
    assert all(isinstance(cat, typecheck) for cat in cats_to_keep)
    if cats_to_keep and len(cats_to_keep):
        mapping_dict = {c: c for c in cats_to_keep}
    else:
        mapping_dict = {}
    new_cat_dict = coco_dict["categories"]
    if typecheck == str:
        print("string?")
        return map_cat(
            coco_dict, new_cat_dict, mapping_dict, keep_old=False, map_is_id=False
        )
    elif typecheck == int:
        print("int?")
        return map_cat(
            coco_dict, new_cat_dict, mapping_dict, keep_old=False, map_is_id=True
        )
    else:
        raise NotImplementedError
