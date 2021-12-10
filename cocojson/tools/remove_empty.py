"""
Remove empty/negative images from COCO JSON, aka images without associated annotations.

Original image IDs are preserved. 
"""

from cocojson.utils.common import read_coco_json, write_json_in_place


def remove_empty_from_files(coco_json, out_json=None):
    coco_dict, _ = read_coco_json(coco_json)
    out_dict = remove_empty(coco_dict)
    write_json_in_place(coco_json, out_dict, append_str="noempty", out_json=out_json)


def remove_empty(coco_dict):
    wanted_imgs = [annot["image_id"] for annot in coco_dict["annotations"]]
    new_imgs = [img for img in coco_dict["images"] if img["id"] in wanted_imgs]
    coco_dict["images"] = new_imgs
    return coco_dict
