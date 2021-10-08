"""
Split up a COCO JSON file by images into N sets defined by ratio of total images

To shuffle images, flag `shuffle=True`

"""
from collections import defaultdict
from copy import deepcopy
from itertools import accumulate

from random import shuffle

from cocojson.utils.common import read_coco_json, write_json_in_place


def split_from_file(cocojson, ratios, names=None, do_shuffle=False):
    coco_dict, setname = read_coco_json(cocojson)
    split_coco_dicts = split(
        coco_dict, ratios, names=names, do_shuffle=do_shuffle, setname=setname
    )

    for name, new_cocodict in split_coco_dicts.items():
        write_json_in_place(cocojson, new_cocodict, append_str=name)


def default_coco_dict():
    new_dict = {
        "images": [],
        "annotations": [],
    }
    return new_dict


def split(coco_dict, ratios, names=None, do_shuffle=False, setname=""):
    assert sum(ratios) == 1.0, "Ratios given does not sum up to 1.0"
    if names:
        assert len(ratios) == len(names)
    else:
        names = [f"split{i}" for i in range(len(ratios))]

    total_imgs = len(coco_dict["images"])
    print(f"Total imgs: {total_imgs}")
    splits_num = [int(round(x * total_imgs)) for x in ratios]
    assert sum(splits_num) == total_imgs
    print(f"Splitting into {splits_num}")
    splits_num[0] -= 1
    splits_acc = list(accumulate(splits_num))
    assert splits_acc[-1] == total_imgs - 1

    if do_shuffle:
        shuffle(coco_dict["images"])

    split_coco_dicts = defaultdict(default_coco_dict)
    img_ids_maps = defaultdict(dict)
    oldimgid2name = {}
    split_idx = 0
    this_name = names[split_idx]
    this_split_images = split_coco_dicts[this_name]["images"]
    this_img_ids_map = img_ids_maps[this_name]
    for i, img_dict in enumerate(coco_dict["images"]):
        oldimgid2name[img_dict["id"]] = this_name

        new_img_dict = deepcopy(img_dict)
        new_img_id = len(this_split_images) + 1

        this_img_ids_map[img_dict["id"]] = new_img_id
        new_img_dict["id"] = new_img_id
        this_split_images.append(new_img_dict)

        if i >= splits_acc[split_idx]:
            if split_idx == len(splits_acc) - 1:
                break
            else:
                split_idx += 1
                this_name = names[split_idx]
                this_split_images = split_coco_dicts[this_name]["images"]
                this_img_ids_map = img_ids_maps[this_name]

    for annot_dict in coco_dict["annotations"]:
        name = oldimgid2name[annot_dict["image_id"]]
        new_annot_dict = deepcopy(annot_dict)
        new_annot_dict["id"] = len(split_coco_dicts[name]["annotations"]) + 1
        new_annot_dict["image_id"] = img_ids_maps[name][annot_dict["image_id"]]
        split_coco_dicts[name]["annotations"].append(new_annot_dict)

    for name, dic in split_coco_dicts.items():
        if "info" in coco_dict:
            dic["info"] = deepcopy(coco_dict["info"])
            dic["info"]["description"] = f"{setname}_{name}"
        if "licenses" in coco_dict:
            dic["licenses"] = deepcopy(coco_dict["licenses"])
        if "categories" in coco_dict:
            dic["categories"] = deepcopy(coco_dict["categories"])

    return split_coco_dicts
