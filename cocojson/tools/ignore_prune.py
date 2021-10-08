"""
Remove images annotated with certain "ignore" category labels. This is usually used for removing rubbish images that are pointed out by annotators to ignore frame.

Default ignore_list = ["ignore"]

"ignore" labels will ignore entire image, take out image and associated annotations. "ignore" labels also taken out from categories

If img_root is given, ignored images will be deleted from the img_root. By default when img_root is not given, nothing will happen to the actual ignored image files, just taken out from the coco json.

"""
from warnings import warn
from os import remove

from cocojson.utils.common import read_coco_json, write_json_in_place, path


def ignore_prune_from_file(
    coco_json, ignore_list=["ignore"], out_json=None, img_root=None
):
    coco_dict, _ = read_coco_json(coco_json)
    out_dict, num_pruned = ignore_prune(
        coco_dict, ignore_list=ignore_list, img_root=img_root
    )
    write_json_in_place(coco_json, out_dict, append_str="pruned", out_json=out_json)
    return num_pruned


def ignore_prune(coco_dict, ignore_list=["ignore"], img_root=None):
    if img_root:
        img_root = path(img_root, is_dir=True)

    print(f"Ignore labels: {ignore_list}")
    new_cats = []
    cat_indices_map = {}
    ignore_cat_ids = []
    for cat in coco_dict["categories"]:
        if cat["name"] in ignore_list:
            cat_indices_map[cat["id"]] = None
            ignore_cat_ids.append(cat["id"])
        else:
            new_id = len(new_cats) + 1
            cat_indices_map[cat["id"]] = new_id
            cat["id"] = new_id
            new_cats.append(cat)
    coco_dict["categories"] = new_cats

    remove_img_ids = [
        annot["image_id"]
        for annot in coco_dict["annotations"]
        if annot["category_id"] in ignore_cat_ids
    ]

    new_imgs = []
    img_ids_map = {}
    orig_num_imgs = len(coco_dict["images"])
    for img_dict in coco_dict["images"]:
        if img_dict["id"] in remove_img_ids:
            if img_root is not None:
                img_path = img_root / img_dict["file_name"]
                if img_path.is_file():
                    remove(img_path)
                    print(f"Removed {img_path}")
                else:
                    warn(
                        f"Image is supposed to be ignored and pruned, but it already does not exist: {img_path}"
                    )
        else:
            new_img_id = len(new_imgs) + 1
            img_ids_map[img_dict["id"]] = new_img_id
            img_dict["id"] = new_img_id
            new_imgs.append(img_dict)
    coco_dict["images"] = new_imgs
    num_pruned = orig_num_imgs - len(new_imgs)
    print(f"Pruned {num_pruned} imgs due to ignore labels.")
    print(f"Final Total Imgs: {len(new_imgs)}")

    new_annots = []
    for annot in coco_dict["annotations"]:
        if annot["image_id"] in img_ids_map:
            annot["id"] = len(new_annots) + 1
            annot["image_id"] = img_ids_map[annot["image_id"]]
            annot["category_id"] = cat_indices_map[annot["category_id"]]
            new_annots.append(annot)
    coco_dict["annotations"] = new_annots

    return coco_dict, num_pruned
