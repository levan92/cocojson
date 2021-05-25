'''
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
'''

from pathlib import Path
from datetime import date

from cocojson.utils.common import read_coco_json, write_json, assure_copy

def merge_cats_get_id(cats, this_cat):
    for cat in cats:
        if cat['name'] == this_cat['name']:
            return cat['id']
    else:
        this_cat['id'] = len(cats)+1
        cats.append(this_cat)
        return this_cat['id']            

def merge(jsons, img_roots, cids, output_dir, outname='merged'):
    assert(len(img_roots) == len(jsons))
    assert(len(img_roots) == len(cids))

    out_dir_path = Path(output_dir)
    out_image_dir = out_dir_path / 'images'

    current_image_id = 1
    current_annot_id = 1
    merged_dict = {'info': {'description':'','data_created':f'{date.today():%Y/%m/%d}'}, 'annotations': [], 'categories': [], 'images': []}
    merged_names = []
    for i, (json_path, images_dir_path, cids_to_merge) in enumerate(zip(jsons, img_roots, cids)):
        cocodict, set_name = read_coco_json(json_path)
        merged_names.append(set_name)

        catid_old2new = {}
        for cat in cocodict['categories']:
            if cat['id'] in cids_to_merge:
                orig_cat_id = cat['id']
                catid_old2new[orig_cat_id] = merge_cats_get_id(merged_dict['categories'], cat)
        
        imgid_old2new = {}
        for img in cocodict['images']:
            imgid_old2new[img['id']] = current_image_id
            img['id'] = current_image_id
            current_image_id += 1

            old_img_path = Path(images_dir_path) / img['file_name']
            img['file_name'] = str( Path(set_name) / img['file_name'] )
            new_img_path = out_image_dir / img['file_name']

            assure_copy(old_img_path, new_img_path)
            # print(f'{old_img_path} >>> {new_img_path}')

            merged_dict['images'].append(img)

        for annot in cocodict['annotations']:
            if int(annot['category_id']) in cids_to_merge:
                annot['id'] = current_annot_id
                current_annot_id += 1
                annot['image_id'] = imgid_old2new[annot['image_id']]
                annot['category_id'] = catid_old2new[annot['category_id']]
                merged_dict['annotations'].append(annot)
    
    merged_dict['info']['description'] = '+'.join(merged_names)
    
    out_json = out_dir_path / f'{outname}.json'
    write_json(out_json, merged_dict)

