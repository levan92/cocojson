# CrowdHuman odgt to COCO JSON

Converts CrowdHuman dataset's odgt annotation format to COCO JSON format

Extracted from https://www.crowdhuman.org/download.html:

odgt is a file format that each line of it is a JSON, this JSON contains the whole annotations for the relative image. 
```
JSON{
    "ID" : image_filename,
    "gtboxes" : [gtbox], 
}

gtbox{
    "tag" : "person" or "mask", 
    "vbox": [x, y, w, h],
    "fbox": [x, y, w, h],
    "hbox": [x, y, w, h],
    "extra" : extra, 
    "head_attr" : head_attr, 
}

extra{
    "ignore": 0 or 1,
    "box_id": int,
    "occ": int,
}

head_attr{
    "ignore": 0 or 1,
    "unsure": int,
    "occ": int,
}
```
- mask tag means that this box is crowd/reflection/something like person/... and needs to be ignored (the ignore in extra is 1)
- vbox, fbox, hbox means visible box, full box, head box respectively

@article{shao2018crowdhuman,
    title={CrowdHuman: A Benchmark for Detecting Human in a Crowd},
    author={Shao, Shuai and Zhao, Zijian and Li, Boxun and Xiao, Tete and Yu, Gang and Zhang, Xiangyu and Sun, Jian},
    journal={arXiv preprint arXiv:1805.00123},
    year={2018}
}

## Usage

```bash
python3 -m cocojson.run.crowdhuman2coco -h
```

```
usage: crowdhuman2coco.py [-h] [--outjson OUTJSON] odgt root

positional arguments:
  odgt               Path to CrowdHuman odgt file
  root               Path to images root directory

optional arguments:
  -h, --help         show this help message and exit
  --outjson OUTJSON  Path to output json. Defaults to "<task_name>.json"
                     sibling to given root directory.
```

## Examples

```bash
python3 -m cocojson.run.crowdhuman2coco /data/CrowdHuman/annotation_val.odgt /data/CrowdHuman/val_images
```
