import json
from shutil import copy
from pathlib import Path
from collections import defaultdict
import filecmp
from functools import reduce
from operator import getitem

IMG_EXTS = [".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp", ".gif", ".webp"]
IMG_EXTS = [x.lower() for x in IMG_EXTS] + [x.upper() for x in IMG_EXTS]


def read_json(json_path):
    with open(json_path, "r") as f:
        d = json.load(f)
    return d


def write_json(json_path, dic):
    with open(json_path, "w") as f:
        json.dump(dic, f)
    print(f"Wrote json to {json_path}")


def path(str_path, is_dir=False, mkdir=False):
    path_ = Path(str_path)
    if is_dir:
        if mkdir:
            path_.mkdir(parents=True, exist_ok=True)
        assert path_.is_dir(), path_
    else:
        assert path_.is_file(), path_
    return path_


def assure_copy(src, dst):
    assert Path(src).is_file()
    if Path(dst).is_file() and filecmp.cmp(src, dst, shallow=True):
        return
    Path(dst).parent.mkdir(exist_ok=True, parents=True)
    copy(src, dst)


def get_imgnames_dict(coco_dict_images):
    return {d["id"]: d["file_name"] for d in coco_dict_images}


def get_img2annots(coco_dict_annots):
    img2annots = defaultdict(list)
    for annot in coco_dict_annots:
        img2annots[annot["image_id"]].append(annot)
    return img2annots


def get_ltrbwh(bbox):
    l, t, w, h = bbox
    r = l + w
    b = t + h
    ltrbwh = [int(x) for x in [l, t, r, b, w, h]]
    return ltrbwh


def get_setname(cocodict, json_path):
    try:
        set_name = cocodict["info"]["description"]
        print(f"Processing {set_name} (name from json info description)")
    except KeyError:
        json_path_p = Path(json_path)
        set_name = f"{json_path_p.parent.stem}_{json_path_p.stem}"
        print(f"Processing {set_name} (name derived from json path)")
    return set_name


def get_flatten_name(subpath):
    subpath = Path(subpath)
    elems = [d.stem for d in subpath.parents if d.stem][::-1]
    elems.append(subpath.stem)
    return "_".join(elems)


def read_coco_json(coco_json):
    coco_dict = read_json(coco_json)
    setname = get_setname(coco_dict, coco_json)
    return coco_dict, setname


def get_imgs_from_dir(dirpath):
    return sorted(
        [img for img in dirpath.rglob("*") if img.is_file() and img.suffix in IMG_EXTS]
    )


def dict_val_from_keys_list(dic, keys_list):
    return reduce(getitem, keys_list, dic)


def write_json_in_place(orig_coco_json, coco_dict, append_str="new", out_json=None):
    if out_json is None:
        orig_json_path = Path(orig_coco_json)
        out_json_path = (
            orig_json_path.parent / f"{orig_json_path.stem}_{append_str}.json"
        )
    else:
        out_json_path = Path(out_json)
    write_json(out_json_path, coco_dict)


def parse(json_path, imgroot, outdir=None):
    json_path = path(json_path)
    imgroot_path = path(imgroot, is_dir=True)

    coco_dict = read_json(json_path)

    if outdir:
        outdir = Path(outdir)
        outroot_path = outdir / "images"
        outroot_path.mkdir(exist_ok=True, parents=True)
        return coco_dict, json_path, imgroot_path, outdir, outroot_path
    else:
        return coco_dict, json_path, imgroot_path
