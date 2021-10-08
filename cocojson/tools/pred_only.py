"""
Get annotations/predictions only from a COCO JSON. Usually used to generate a list of predictions for COCO evaluation.

if `add_score` is None (default), no score is added to annotation. Else, `add_score` should be a float, in which the score will be added to each annotation. 
"""
from cocojson.utils.common import path, read_coco_json, write_json


def pred_only(coco_json, add_score=None):
    coco_json_path = path(coco_json)
    coco_dict, setname = read_coco_json(coco_json_path)
    if add_score is not None:
        assert isinstance(add_score, float)
        for annot in coco_dict["annotations"]:
            annot["score"] = add_score
    annotations = coco_dict["annotations"]
    out = coco_json_path.parent / f"{coco_json_path.stem}_pred.json"
    write_json(out, annotations)
