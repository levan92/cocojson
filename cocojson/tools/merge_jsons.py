'''
Merge multiple coco jsons. Assumes image ids are unique across multiple jsons and will also preserve image ids when merging

For example, for merging json files provided by https://www.sama.com/sama-coco-dataset/.
'''

from pathlib import Path 
from tqdm import tqdm 

from cocojson.utils.common import read_coco_json, write_json

def merge_jsons_files(
    dir_of_jsons,
):
    coco_dicts = []
    dir_of_jsons = Path(dir_of_jsons)
    for coco_json in dir_of_jsons.glob('*.json'):
        coco_dicts.append(read_coco_json(coco_json)[0])

    out_dict = merge_jsons(coco_dicts)

    out_json = dir_of_jsons.parent / f'{dir_of_jsons.stem}.json'
    write_json(out_json, out_dict)

def merge_jsons(coco_dicts):
    merged_dict = coco_dicts[0]
    img_ids = [ img_dict['id'] for img_dict in merged_dict['images'] ]
    for coco_dict in tqdm(coco_dicts[1:]):
        for img_dict in coco_dict['images']:
            assert img_dict['id'] not in img_ids
            merged_dict['images'].append(img_dict)
            img_ids.append(img_dict['id'])
        merged_dict['annotations'].extend(coco_dict['annotations'])
    return merged_dict