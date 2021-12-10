"""
Mapping categories to a new dataset. Usually used for converting annotation labels to actual class label for training.
- New categories are defined in a json file in coco format
- Mapping is also defined in another json file, a dict of old label names to new label names. Multiple old label names can map to same new label name.
    Either in Category Names, for e.g.:
       {
            "child": "human",
            "adult": "human",
            "chihuahua" : "dog",
            "bulldog": "dog",
        }
    Or in Category ID (You will need to flag `map_is_id`), for e.g.:
    {
        "1":1,
        "2":1,
        "3":2,
        "4":2
    }

- By default, any old label names not given in mapping will be taken out in the new dataset along with associated annotations. To preserve old label names in the new dataset, please flag `keep_old`. 
"""
from warnings import warn

from cocojson.utils.common import read_coco_json, read_json, write_json_in_place


def normalise_map_dict(mapping_dict, old_cats, new_cats, map_is_id):
    old_id_to_name = {cat["id"]: cat["name"] for cat in old_cats}
    new_id_to_name = {cat["id"]: cat["name"] for cat in new_cats}
    if map_is_id:
        new_map_dict = {
            old_id_to_name[int(old_id)]: new_id_to_name[int(new_id)]
            for old_id, new_id in mapping_dict.items()
        }
        return new_map_dict
    else:
        for old_name, new_name in mapping_dict.items():
            assert new_name in new_id_to_name.values()
        return mapping_dict


def map_cat_from_files(
    coco_json,
    new_cat_json,
    mapping_json,
    out_json=None,
    keep_old=False,
    map_is_id=False,
):
    coco_dict, _ = read_coco_json(coco_json)
    new_cat_dict = read_json(new_cat_json)
    mapping_dict = read_json(mapping_json)

    out_dict = map_cat(
        coco_dict, new_cat_dict, mapping_dict, keep_old=keep_old, map_is_id=map_is_id
    )

    write_json_in_place(coco_json, out_dict, append_str="mapped", out_json=out_json)


def map_cat(
    coco_dict,
    new_cat_dict,
    mapping_dict,
    keep_old=False,
    map_is_id=False,
    warn_verbose=True,
):
    new_cat_list = (
        new_cat_dict["categories"] if isinstance(new_cat_dict, dict) else new_cat_dict
    )
    assert isinstance(new_cat_list, list), new_cat_list
    new_name2cat = {cat["name"]: cat for cat in new_cat_list}

    mapping_dict = normalise_map_dict(
        mapping_dict, coco_dict["categories"], new_cat_list, map_is_id
    )

    new_cats = []
    new_name_to_new_cat = {}
    indices_map = {}
    for cat in coco_dict["categories"]:
        if cat["name"] in mapping_dict:
            new_cat_name = mapping_dict[cat["name"]]
            if new_cat_name in new_name_to_new_cat:
                # new cat already created
                indices_map[cat["id"]] = new_name_to_new_cat[new_cat_name]["id"]
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
            if warn_verbose:
                warn(
                    f"Category: {cat['name']} not found in mapping. Will be removing associated annotation. To keep, please flag keep old."
                )
            continue
        new_id = len(new_cats) + 1
        indices_map[cat["id"]] = new_id
        this_cat["id"] = new_id
        new_cats.append(this_cat)
    coco_dict["categories"] = new_cats

    new_annots = []
    for annot in coco_dict["annotations"]:
        if annot["category_id"] in indices_map:
            annot["category_id"] = indices_map[annot["category_id"]]
            new_annots.append(annot)
    coco_dict["annotations"] = new_annots

    return coco_dict
