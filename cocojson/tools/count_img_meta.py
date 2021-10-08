"""
Count images based on image meta-info/attribute

If attribute is not present for any of the images, it will be placed to "nil". 
"""
from collections import defaultdict

from cocojson.utils.common import dict_val_from_keys_list


def count(coco_dict, meta_keys_list, setname=""):
    counts = defaultdict(int)
    for img_dict in coco_dict["images"]:
        try:
            attr = dict_val_from_keys_list(img_dict, meta_keys_list)
        except KeyError:
            attr = "nil"
        counts[attr] += 1
    return counts
