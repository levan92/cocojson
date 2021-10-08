"""
Converts Custom Object Detection Logging format to COCO. 

This logging format is optimised for real-time logging of OD predictions. 

    The main annotations are described in a text file:
    <frame 1 info>
    <frame 2 info> 
    ...

    For each frame info:
    <frame image name> <bbox 1 info> <bbox 2 info> ...  

    For each bbox info:
    left,top,right,bot,class_id

    For example:
    frame1.jpg 10,10,50,50,0 
    frame2.jpg 14,13,51,52,0 20,25,80,88,1

Associated to it is a `classes.txt` (path sibling) which is a list of classes whose index correspond to the annotations' class ids (zero indexed)

"""
from datetime import datetime

from PIL import Image
from tqdm import tqdm
from pprint import pprint

from cocojson.utils.common import path, write_json


def convert(log_annot, img_root, outjson=None):
    annot_txt_path = path(log_annot)
    annot_root = annot_txt_path.parent
    annot_images_dir = path(img_root, is_dir=True)

    date_dt = datetime.now().date()
    date_str = f"{date_dt:%Y/%m/%d}"
    info_dict = {"description": f"{annot_root.stem}", "data_converted": date_str}
    coco_dict = {
        "info": info_dict,
    }

    annot_classes = annot_root / "classes.txt"
    cid_map = {}
    if annot_classes.is_file():
        with annot_classes.open("r") as f:
            classes = [c.strip() for c in f.readlines()]
            category_dicts = [
                {"id": i + 1, "name": cl, "supercategory": ""}
                for i, cl in enumerate(classes)
            ]
        pprint(category_dicts)
        coco_dict["categories"] = category_dicts

    img_dicts = []
    annot_dicts = []
    with annot_txt_path.open("r") as f:
        for line in tqdm(f.readlines()):
            line = line.strip()
            line = line[:-1] if line[-1] == ";" else line
            splits = line.split()

            imgname = splits[0]
            imgpath = annot_images_dir / imgname
            im = Image.open(str(imgpath))
            iw, ih = im.size
            assert iw > 0
            assert ih > 0
            img_id = len(img_dicts) + 1
            image_dict = {"id": img_id, "width": iw, "height": ih, "file_name": imgname}
            img_dicts.append(image_dict)

            bbs = splits[1:]
            for bb in bbs:
                bb_splits = bb.split(",")[:5]
                x_min, y_min, x_max, y_max, class_id = [
                    int(float(x)) for x in bb_splits
                ]
                w = x_max - x_min
                h = y_max - y_min
                area = w * h
                annot = {
                    "id": len(annot_dicts) + 1,
                    "image_id": img_id,
                    "category_id": class_id + 1,
                    "area": area,
                    "bbox": [x_min, y_min, w, h],
                    "iscrowd": 0,
                }
                annot_dicts.append(annot)

    print(f"{len(annot_dicts)} boxes in {len(img_dicts)} images from {annot_root}")

    coco_dict["images"] = img_dicts
    coco_dict["annotations"] = annot_dicts

    if outjson:
        out_json = outjson
    else:
        json_file_name = annot_root.stem
        out_json = annot_images_dir.parent / f"{json_file_name}.json"
    write_json(out_json, coco_dict)
