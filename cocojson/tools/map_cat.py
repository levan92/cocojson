'''
Mapping categories to a new dataset. Usually used for converting annotation labels to actual class label for training.
- New categories are defined in a json file in coco format
- Mapping is also defined in another json file, a dict of old label names to new label names. Multiple old label names can map to same new label name.

    For example: 
       {
            "child": "human",
            "adult": "human",
            "chihuahua" : "dog",
            "bulldog": "dog",
        }

- By default, any old label names not given in mapping will be taken out in the new dataset along with associated annotations. To preserve old label names in the new dataset, please flag `keep_old`. 
'''

from pathlib import Path
from warnings import warn

from cocojson.utils.common import read_coco_json, read_json, write_json

def map_cat_from_files(coco_json, new_cat_json, mapping_json, out_json=None, keep_old=False):
    coco_dict, setname = read_coco_json(coco_json)
    new_cat_dict = read_json(new_cat_json)
    mapping_dict = read_json(mapping_json)

    out_dict = map_cat(coco_dict, new_cat_dict, mapping_dict, keep_old=keep_old, setname=setname)
    
    if out_json is None:
        orig_json_path = Path(coco_json)
        out_json_path = orig_json_path.parent / f'{orig_json_path.stem}_mapped.json'
    else:
        out_json_path = Path(out_json)
    write_json(out_json_path, out_dict)

def map_cat(coco_dict, new_cat_dict, mapping_dict, keep_old=False, setname=None):
    new_cat_list = new_cat_dict['categories'] if isinstance(new_cat_dict, dict) else new_cat_dict
    assert isinstance(new_cat_list, list),new_cat_list
    new_name2cat = { cat['name']:cat for cat in new_cat_list }

    new_cats = []
    new_name_to_new_cat = {}
    indices_map = {}
    for cat in coco_dict['categories']:
        if cat['name'] in mapping_dict:
            new_cat_name = mapping_dict[cat['name']]
            if new_cat_name in new_name_to_new_cat:
                # new cat already created 
                indices_map[cat['id']] = new_name_to_new_cat[new_cat_name]['id']
                continue
            else:
                # create new cat
                this_cat = new_name2cat[new_cat_name]
                new_name_to_new_cat[new_cat_name] = this_cat
        elif keep_old:
            # not mention in mapping, but keeping
            this_cat = cat
        else:
            # not mention in mapping and throwing away
            warn(f"Category: {cat['name']} not found in mapping. Will be removing associated annotation. To keep, please flag keep old.")
            continue 
        new_id = len(new_cats)+1
        indices_map[cat['id']] = new_id
        this_cat['id'] = new_id
        new_cats.append(this_cat)
    coco_dict['categories'] = new_cats

    new_annots = []
    for annot in coco_dict['annotations']:
        if annot['category_id'] in indices_map:
            annot['category_id'] = indices_map[annot['category_id']]
            new_annots.append(annot)
    coco_dict['annotations'] = new_annots

    return coco_dict
