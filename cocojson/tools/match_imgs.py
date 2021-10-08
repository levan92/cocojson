"""
Match images between COCO JSON A and COCO JSON B. Any images in JSON B that is not found in JSON A will be removed (along with associated annotations)

Match will be through image `file_name`.
"""
from warnings import warn

from cocojson.utils.common import read_coco_json, write_json_in_place


def match_imgs_from_file(cocojsonA, cocojsonB, outjson=None):
    coco_dictA, setnameA = read_coco_json(cocojsonA)
    coco_dictB, setnameB = read_coco_json(cocojsonB)

    trimmed_cocodict = match_imgs(coco_dictA, coco_dictB)

    write_json_in_place(
        cocojsonB, trimmed_cocodict, append_str="trimmed", out_json=outjson
    )


def match_imgs(coco_dictA, coco_dictB):
    imgs_A = [img["file_name"] for img in coco_dictA["images"]]

    new_imgs = []
    present_imgs = []
    img_id_map = {}
    for img in coco_dictB["images"]:
        if img["file_name"] in imgs_A:
            new_img_id = len(new_imgs) + 1
            img_id_map[img["id"]] = new_img_id
            img["id"] = new_img_id
            new_imgs.append(img)
            present_imgs.append(img["file_name"])
    coco_dictB["images"] = new_imgs

    remainder = set(imgs_A) - set(present_imgs)
    if len(remainder) > 0:
        warn(
            f"The following images are present in reference coco json (cocojsonA) but not in coco json to be trimmed (cocojsonB): {remainder}"
        )

    new_annots = []
    for annot in coco_dictB["annotations"]:
        if annot["image_id"] in img_id_map:
            annot["image_id"] = img_id_map[annot["image_id"]]
            new_annot_id = len(new_annots) + 1
            annot["id"] = new_annot_id
            new_annots.append(annot)
    coco_dictB["annotations"] = new_annots

    return coco_dictB
