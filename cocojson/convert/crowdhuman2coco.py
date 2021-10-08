"""
Converts CrowdHuman dataset's odgt annotation format to COCO JSON format

Extracted from https://www.crowdhuman.org/download.html:

odgt is a file format that each line of it is a JSON, this JSON contains the whole annotations for the relative image. We prefer using this format since it is reader-friendly.

JSON{
    "ID" : image_filename,
    "gtboxes" : [gtbox], 
}

gtbox{
    "tag" : "person" or "mask", 
    "vbox": [x, y, w, h],
    "fbox": [x, y, w, h],
    "hbox": [x, y, w, h],
    "extra" : extra, 
    "head_attr" : head_attr, 
}

extra{
    "ignore": 0 or 1,
    "box_id": int,
    "occ": int,
}

head_attr{
    "ignore": 0 or 1,
    "unsure": int,
    "occ": int,
}
- tag is mask means that this box is crowd/reflection/something like person/... and need to be ignore(the ignore in extra is 1)
- vbox, fbox, hbox means visible box, full box, head box respectively

@article{shao2018crowdhuman,
    title={CrowdHuman: A Benchmark for Detecting Human in a Crowd},
    author={Shao, Shuai and Zhao, Zijian and Li, Boxun and Xiao, Tete and Yu, Gang and Zhang, Xiangyu and Sun, Jian},
    journal={arXiv preprint arXiv:1805.00123},
    year={2018}
}

Code adapted from https://github.com/hasanirtiza/Pedestron/blob/master/tools/convert_datasets/crowdhuman/convert_crowdhuman_to_coco.py
"""
import json
from pathlib import Path

from PIL import Image
from tqdm import tqdm

from cocojson.utils.common import path, write_json


def convert(odgt_file, image_root, outjson=None):
    odgt_path = path(odgt_file)
    with open(odgt_path, "r") as f:
        records = [
            json.loads(line.strip("\n")) for line in f.readlines()
        ]  # str to list

    image_root = path(image_root, is_dir=True)

    coco_dict = {
        "info": {"description": f"Converted from {Path(odgt_file).name}(CrowdHuman)"},
        "annotations": [],
        "categories": [],
        "images": [],
    }
    cat2catid = {}
    for record in tqdm(records):
        imgsubpath = f"{record['ID']}.jpg"
        imgpath = image_root / imgsubpath
        img = Image.open(imgpath)
        img_dict = {
            "file_name": imgsubpath,
            "height": img.size[1],
            "width": img.size[0],
            "id": len(coco_dict["images"]) + 1,
        }
        coco_dict["images"].append(img_dict)

        for gt_box in record["gtboxes"]:
            cat = gt_box["tag"]
            if cat not in cat2catid:
                cat2catid[cat] = len(cat2catid) + 1
            cat_id = cat2catid[cat]
            fbox = gt_box["fbox"]
            ignore = 0
            if "ignore" in gt_box["extra"]:
                ignore = gt_box["extra"]["ignore"]
            annotation = {
                "id": len(coco_dict["annotations"]) + 1,
                "image_id": img_dict["id"],
                "category_id": cat_id,
                "bbox": fbox,
                "area": fbox[2] * fbox[3],
                "hbox": gt_box["hbox"],
                "vbox": gt_box["vbox"],
                "iscrowd": ignore,
                "ignore": ignore,
            }
            if "occ" in gt_box["extra"]:
                annotation["attributes"] = {"occluded": gt_box["extra"]["occ"]}
            coco_dict["annotations"].append(annotation)

    for catname, catid in sorted(cat2catid.items(), key=lambda x: x[1]):
        cat_dict = {
            "id": catid,
            "name": catname,
            "supercategory": "",
        }
        coco_dict["categories"].append(cat_dict)

    if outjson:
        out_json = outjson
    else:
        out_json = odgt_path.parent / f"{odgt_path.stem}.json"
    write_json(out_json, coco_dict)
