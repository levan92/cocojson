"""
Visualise annotations from a coco json dataset. 

"""

from pathlib import Path
from random import sample
from collections import defaultdict

from tqdm import tqdm
import cv2

from cocojson.utils.common import (
    path,
    read_coco_json,
    get_img2annots,
    get_flatten_name,
    get_imgnames_dict,
)
from cocojson.utils.draw import draw_annot


def viz(json, root, outdir=None, sample_k=None, show=False):
    img_root = path(root, is_dir=True)
    coco_dict, setname = read_coco_json(json)
    img2annots = get_img2annots(coco_dict["annotations"])

    if outdir is not None:
        if isinstance(outdir, str):
            outdir = Path(outdir)
        else:
            outdir = Path(json).parent / "viz"
        outdir.mkdir(exist_ok=True, parents=True)

    if sample_k:
        assert sample_k > 0, "Sample must be a positive int"
        image_dicts = sample(coco_dict["images"], sample_k)
    else:
        image_dicts = coco_dict["images"]

    for img_dict in tqdm(image_dicts):
        imgpath = img_root / img_dict["file_name"]
        assert imgpath.is_file(), imgpath
        img = cv2.imread(str(imgpath))
        img_show = img.copy()
        for annot in img2annots[img_dict["id"]]:
            draw_annot(img_show, annot)
        if show:
            cv2.imshow(f"{setname}", img_show)
            cv2.waitKey(0)
        if outdir:
            uniq_name = get_flatten_name(img_dict["file_name"])
            writepath = outdir / f"{uniq_name}_viz.jpg"
            cv2.imwrite(str(writepath), img_show)

    num_images = len(image_dicts)
    num_annots = len(coco_dict["annotations"])
    return num_images, num_annots


def viz_individual_box(json, root, outdir, color=(255, 255, 0), thickness=1, buffer=0):
    """
    Highly specific case of visualising each bbs as one image and reporting the bb info in the filename.
    """
    outdir = path(outdir, is_dir=True, mkdir=True)
    img_root = path(root, is_dir=True)
    coco_dict, setname = read_coco_json(json)
    imgid2filename = get_imgnames_dict(coco_dict["images"])
    imgid2shipcount = defaultdict(int)
    for annot in tqdm(coco_dict["annotations"]):
        img_file_name = imgid2filename[annot["image_id"]]
        img_path = img_root / img_file_name
        assert img_path.is_file
        imgid2shipcount[annot["image_id"]] += 1

        img = cv2.imread(str(img_path))
        img_show = img.copy()
        l, t, r, b = draw_annot(
            img_show, annot, color=color, thickness=thickness, buffer=buffer
        )
        ship_idx = imgid2shipcount[annot["image_id"]] - 1
        out_img_path = (
            outdir
            / f"{img_path.stem}_ship{ship_idx}_ltrb{int(l)},{int(t)},{int(r)},{int(b)}.jpg"
        )
        cv2.imwrite(str(out_img_path), img_show)

    num_images = len(coco_dict["images"])
    num_annots = len(coco_dict["annotations"])
    return num_images, num_annots
