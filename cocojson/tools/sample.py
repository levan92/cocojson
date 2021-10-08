"""
Samples k images from a dataset. 

Expected format of 1 x Dataset:
    - 1 x json file 
    - 1 x Image Folder (to get to the image, path is assumed to be "Image Folder"/"file_name" given in json)

Will output new dataset in given `outdir`, with new json file (same name as original json name) and `images` directory. 
"""

from collections import defaultdict
from shutil import copy
from random import sample as _sample
from tqdm import tqdm

from cocojson.utils.common import read_json, write_json, parse


def sample(json_path, imgroot, outdir, k=10):
    coco_dict, json_path, imgroot_path, outdir, outroot_path = parse(
        json_path, imgroot, outdir
    )

    assert k > 0

    coco_dict = read_json(json_path)

    if k > len(coco_dict["images"]):
        sampled = coco_dict["images"]
    else:
        sampled = _sample(coco_dict["images"], k)

    new_imgs = []
    chosen_img_ids = []
    for img_dict in sampled:
        imgpath = imgroot_path / img_dict["file_name"]
        assert imgpath.is_file()

        newip = outroot_path / img_dict["file_name"]
        newip.parent.mkdir(exist_ok=True, parents=True)

        # print(f'{imgpath}-->{newip}')
        copy(imgpath, newip)

        chosen_img_ids.append(img_dict["id"])
        new_imgs.append(img_dict)

    new_annots = []
    for annot in coco_dict["annotations"]:
        if annot["image_id"] in chosen_img_ids:
            new_annots.append(annot)

    coco_dict["images"] = new_imgs
    coco_dict["annotations"] = new_annots

    out_json = outdir / json_path.name
    write_json(out_json, coco_dict)


def sample_by_class(
    json_path, imgroot, outdir, class_ks=10, max_img=None, retries=1000
):
    """
    class_ks : How many to sample for each category. Integer to apply to all categories, or a list of integers corresponding to the categories.
    max_img :  Max num of images to be sampled, will retry until it falls below
    retires: Max number of retries
    """
    coco_dict, json_path, imgroot_path, outdir, outroot_path = parse(
        json_path, imgroot, outdir
    )

    num_cats = len(coco_dict["categories"])
    if isinstance(class_ks, int):
        class_k = class_ks
        class_ks = [class_k for _ in range(num_cats)]
    elif len(class_ks) == 1:
        class_k = class_ks[0]
        class_ks = [class_k for _ in range(num_cats)]
    assert len(class_ks) == num_cats

    some_dict = defaultdict(list)
    for annot in tqdm(coco_dict["annotations"]):
        img_id = annot["image_id"]
        cat_id = annot["category_id"]
        if img_id not in some_dict[cat_id]:
            some_dict[cat_id].append(img_id)

    while True:
        for retry in range(retries):
            sampled_imgs = []
            for imgs, k in zip(some_dict.values(), class_ks):
                if k > len(imgs):
                    sampled = imgs
                else:
                    sampled = _sample(imgs, k)
                sampled_imgs.extend(sampled)
            sampled_imgs = list(set(sampled_imgs))
            if max_img and len(sampled_imgs) > max_img:
                print(
                    f"Current sampling results in more image ({len(sampled_imgs)}) than allowable by max_img ({max_img}) argument, retrying ({retry+1}/{retries}).."
                )
            else:
                break
        else:
            ans = input(f"Try another max_img (current {max_img})? n or give number: ")
            try:
                max_img = int(ans)
                assert max_img > 0
            except ValueError:
                print(f"Using back current max_img: {max_img}")

            ans = input(
                f"Try another class_ks (current {class_ks})? n or give a number: "
            )
            try:
                class_k = int(ans)
                assert class_k > 0
                class_ks = [class_k for _ in range(num_cats)]
            except ValueError:
                print(f"Using back current class_ks: {class_ks}")
            continue
        # raise Exception('Not able to find suitable sampling under the given class sampling size and max num of imgs limit. Please retry.')
        break

    print(f"Sampled dataset will have {len(sampled_imgs)} images")
    new_img_dicts = []
    for img_dict in tqdm(coco_dict["images"]):
        if img_dict["id"] in sampled_imgs:
            imgpath = imgroot_path / img_dict["file_name"]
            assert imgpath.is_file()

            newip = outroot_path / img_dict["file_name"]
            newip.parent.mkdir(exist_ok=True, parents=True)

            # print(f'{imgpath}-->{newip}')
            copy(imgpath, newip)

            new_img_dicts.append(img_dict)

    new_annots = []
    for annot in coco_dict["annotations"]:
        if annot["image_id"] in sampled_imgs:
            new_annots.append(annot)

    coco_dict["images"] = new_img_dicts
    coco_dict["annotations"] = new_annots

    out_json = outdir / json_path.name
    write_json(out_json, coco_dict)
