"""
Merges multiple datasets in coco json format

Expected format of 1 x Dataset:
    - 1 x json file 
    - 1 x Image Folder (to get to the image, path is assumed to be "Image Folder"/"file_name" given in json)

Merged Dataset:
    - 1 x json file ("file_name" will be subpaths, for eg, "Image Folder from DatasetA/image01.png")
    - Master Images Folder 
        - Image Folder from DatasetA
        - Image Folder from DatasetA
        ...

Only given category IDs for each dataset will be merged. Merged category list will merge constituent categories based on category name.
"""

from pathlib import Path
from datetime import date
from collections import defaultdict
from warnings import warn

from cocojson.utils.common import read_coco_json, write_json, assure_copy, path


def merge_cats_get_id(cats, this_cat):
    for cat in cats:
        if cat["name"] == this_cat["name"]:
            return cat["id"]
    else:
        this_cat["id"] = len(cats) + 1
        cats.append(this_cat)
        return this_cat["id"]


def merge(jsons, img_roots, output_dir, cids=None, outname="merged"):
    """
    if `cids` is None, it will merge all cids
    """
    assert len(img_roots) == len(jsons)
    if cids is not None:
        assert len(img_roots) == len(cids)

    out_dir_path = Path(output_dir)
    out_image_dir = out_dir_path / "images"

    current_image_id = 1
    current_annot_id = 1
    merged_dict = {
        "info": {"description": "", "data_created": f"{date.today():%Y/%m/%d}"},
        "annotations": [],
        "categories": [],
        "images": [],
    }
    merged_names = []
    for i, (json_path, images_dir_path) in enumerate(zip(jsons, img_roots)):
        cocodict, set_name = read_coco_json(json_path)
        merged_names.append(set_name)

        if cids is not None:
            cids_to_merge = cids[i]
        catid_old2new = {}
        for cat in cocodict["categories"]:
            if cids is not None and int(cat["id"]) not in cids_to_merge:
                continue
            orig_cat_id = cat["id"]
            catid_old2new[orig_cat_id] = merge_cats_get_id(
                merged_dict["categories"], cat
            )

        imgid_old2new = {}
        for img in cocodict["images"]:
            imgid_old2new[img["id"]] = current_image_id
            img["id"] = current_image_id
            current_image_id += 1

            old_img_path = Path(images_dir_path) / img["file_name"]
            img["file_name"] = str(Path(set_name) / img["file_name"])
            new_img_path = out_image_dir / img["file_name"]

            assure_copy(old_img_path, new_img_path)
            # print(f'{old_img_path} >>> {new_img_path}')

            merged_dict["images"].append(img)

        for annot in cocodict["annotations"]:
            if cids is not None and cat["id"] not in cids_to_merge:
                continue
            annot["id"] = current_annot_id
            current_annot_id += 1
            annot["image_id"] = imgid_old2new[annot["image_id"]]
            annot["category_id"] = catid_old2new[annot["category_id"]]
            merged_dict["annotations"].append(annot)

    merged_dict["info"]["description"] = "+".join(merged_names)

    out_json = out_dir_path / f"{outname}.json"
    write_json(out_json, merged_dict)


def get_dataset_splits_from(mergelist):
    mergelist = path(mergelist)
    splits = defaultdict(list)
    with mergelist.open("r") as f:
        mode = None
        for l in f.readlines():
            l = l.strip()
            if l.startswith("#"):
                continue
            if l == "":
                mode = None
            if l.startswith("["):
                start = l.index("[")
                end = l.index("]")
                mode = l[start + 1 : end]
                mode = mode.casefold()
                if mode in splits:
                    # earlier splits get overwritten
                    splits[mode] = []
                continue
            if mode is not None and l:
                l = l.split(" ")[0]  # ignore any comments after directory name
                splits[mode].append(l)
    return splits


def find_coco_in(grandparent, get_images=True):
    grandparent = path(grandparent, is_dir=True)
    cocos = {}
    for jp in grandparent.rglob("*.json"):
        if jp.stem == jp.parent.stem:
            if get_images:
                imagedir = jp.parent / "images"
                if imagedir.is_dir():
                    cocos[jp.stem] = (jp, imagedir)
            else:
                cocos[jp.stem] = jp
    # for d in grandparent.rglob('images'):
    #     stem = d.parent.stem
    #     cocojson = d.parent / f'{stem}.json'
    #     if cocojson.is_file():
    #         cocos[stem] = (cocojson, d)
    return cocos


def merge_from_file(merge_list, output_dir, root=None):
    """
    This is a way of merging datasets (each in coco format) based on a list file.

    `merge_list` is a txt file which contains a list of coco dataset directories to merge. Each coco dataset directory should have an `images` folder and a `<directory name>.json` annotation file. In the source list file, dataset split modes are indicated by [square brackets], followed by the constituent directory names. An empty lines or new square bracket will indicate the end of the previous split. Directory names must be unique.

    For e.g.:
        [train]
        iphone_dataset1
        iphone_dataset2
        dslr_dataset1
        dslr_dataset2

        [val]
        iphone_dataset3
        dslr_dataset3

    Comments (# in front of line) are ignored

    `root` is the parent folder containing all the coco dataset folders (can be nested, but dataset folder names have to be unique). If not given, will search within `merge_list`'s folder.

    This will merge all categories in all given datasets.
    """

    merge_list_path = path(merge_list)
    ds_splits = get_dataset_splits_from(merge_list_path)

    if root is None:
        root = merge_list_path.parent
    grandparent = path(root, is_dir=True)
    coco_dirs = find_coco_in(grandparent)

    for mode, ds_list in ds_splits.items():
        jsons = []
        img_roots = []
        for ds in ds_list:
            if ds not in coco_dirs:
                warn(f"{ds} given in merge list but not found in root!")
            else:
                json, imgroot = coco_dirs[ds]
                jsons.append(json)
                img_roots.append(imgroot)
        merge(jsons, img_roots, output_dir, cids=None, outname=mode)
