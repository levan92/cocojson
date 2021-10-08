"""
Convert from CVAT Video XML to COCO JSON (with track info intact)
"""

import xml.etree.ElementTree as ET
from datetime import datetime, date
from pathlib import Path

from PIL import Image
from tqdm import tqdm

from cocojson.utils.common import path, get_imgs_from_dir, write_json


def convert(xml_file, img_root, outjson=None):

    tree = ET.parse(xml_file)
    root = tree.getroot()
    meta = root.find("meta")

    task = meta.find("task")
    taskname = task.find("name")
    if taskname is None:
        taskname = ""
    else:
        taskname = taskname.text

    dumped = meta.find("dumped")
    if dumped is None:
        date_str = f"{date.today():%Y/%m/%d}"
    else:
        date_dt = datetime.strptime(dumped.text.split()[0], "%Y-%m-%d").date()
        date_str = f"{date_dt:%Y/%m/%d}"

    start_frame = task.find("start_frame")
    if start_frame is None:
        start_frame = 0
    else:
        start_frame = int(start_frame.text)
    assert start_frame >= 0

    coco_dict = {
        "info": {"description": taskname, "data_created": date_str},
        "annotations": [],
        "categories": [],
        "images": [],
    }

    labels = meta.find("task").find("labels")
    this_cat_id = 1
    cat_name2id = {}
    for label in labels.findall("label"):
        label_name = label.find("name").text
        cat_name2id[label_name] = this_cat_id
        cat_dict = {"id": this_cat_id, "name": label_name, "supercategory": ""}
        this_cat_id += 1
        coco_dict["categories"].append(cat_dict)

    img_root = path(img_root, is_dir=True)
    img_paths = get_imgs_from_dir(img_root)
    this_img_id = 1
    img_idx2id = {}
    for i, img_path in enumerate(img_paths):
        w, h = Image.open(img_path).size
        img_idx2id[i] = this_img_id
        img_dict = {
            "id": this_img_id,
            "file_name": str(img_path.relative_to(img_root)),
            "height": h,
            "width": w,
        }
        this_img_id += 1
        coco_dict["images"].append(img_dict)

    this_annot_id = 1
    for track_elem in tqdm(root.findall("track")):
        tid = int(track_elem.attrib["id"])
        catid = cat_name2id[track_elem.attrib["label"]]
        for box_elem in track_elem.findall("box"):
            if bool(int(box_elem.attrib["outside"])):
                continue
            frame_idx = int(box_elem.attrib["frame"])
            imgid = img_idx2id[frame_idx - start_frame]
            occluded = bool(int(box_elem.attrib["occluded"]))
            keyframe = bool(int(box_elem.attrib["keyframe"]))
            l = float(box_elem.attrib["xtl"])
            t = float(box_elem.attrib["ytl"])
            r = float(box_elem.attrib["xbr"])
            b = float(box_elem.attrib["ybr"])
            w = r - l
            h = b - t
            annot_dict = {
                "id": this_annot_id,
                "image_id": imgid,
                "category_id": catid,
                "bbox": [l, t, w, h],
                "area": w * h,
                "iscrowd": 0,
                "attributes": {
                    "occluded": occluded,
                    "track_id": tid,
                    "keyframe": keyframe,
                },
            }
            this_annot_id += 1
            coco_dict["annotations"].append(annot_dict)

    if outjson:
        out_json = outjson
    else:
        json_file_name = taskname if taskname else Path(xml_file).stem
        out_json = img_root.parent / f"{json_file_name}.json"
    write_json(out_json, coco_dict)
