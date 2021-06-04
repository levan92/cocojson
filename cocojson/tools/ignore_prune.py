'''
Remove images annotated with certain "ignore" category labels. This is usually used for removing rubbish images that are pointed out by annotators to ignore frame.

Default ignore_list = ["ignore"]

"ignore" labels will ignore entire image, take out image and associated annotations. "ignore" labels also taken out from categories

'''
from pathlib import Path

from cocojson.utils.common import read_coco_json, write_json

def ignore_prune_from_file(coco_json, ignore_list=['ignore'], out_json=None):
    coco_dict, setname = read_coco_json(coco_json)
    out_dict = ignore_prune(coco_dict, ignore_list=ignore_list, setname=setname)

    if out_json is None:
        orig_json_path = Path(coco_json)
        out_json_path = orig_json_path.parent / f'{orig_json_path.stem}_pruned.json'
    else:
        out_json_path = Path(out_json)
    write_json(out_json_path, out_dict)

def ignore_prune(coco_dict, ignore_list=['ignore'], setname=None):
    print(f'Ignore labels: {ignore_list}')
    new_cats = []
    cat_indices_map = {}
    ignore_cat_ids = []
    for cat in coco_dict['categories']:
        if cat['name'] in ignore_list:
            cat_indices_map[cat['id']] = None
            ignore_cat_ids.append(cat['id'])
        else:
            new_id = len(new_cats)+1
            cat_indices_map[cat['id']] = new_id
            cat['id'] = new_id
            new_cats.append(cat)        
    coco_dict['categories'] = new_cats

    remove_img_ids = [ annot['image_id'] for annot in coco_dict['annotations'] if annot['category_id'] in ignore_cat_ids ]

    new_imgs = []
    img_ids_map = {}
    orig_num_imgs = len(coco_dict['images'])
    for img_dict in coco_dict['images']:
        if img_dict['id'] not in remove_img_ids:
            new_img_id = len(new_imgs) + 1
            img_ids_map[img_dict['id']] = new_img_id
            img_dict['id'] = new_img_id
            new_imgs.append(img_dict)
    coco_dict['images'] = new_imgs
    print(f'Pruned {orig_num_imgs-len(new_imgs)} imgs due to ignore labels.')
    print(f'Final Total Imgs: {len(new_imgs)}')

    new_annots = []
    for annot in coco_dict['annotations']:
        if annot['image_id'] in img_ids_map:
            annot['id'] = len(new_annots) + 1
            annot['image_id'] = img_ids_map[annot['image_id']]
            annot['category_id'] = cat_indices_map[annot['category_id']]
            new_annots.append(annot)
    coco_dict['annotations'] = new_annots

    return coco_dict