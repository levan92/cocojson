# Custom Object Detection Logging format to COCO JSON

Converts Custom Object Detection Logging format to COCO.

This logging format is optimised for real-time logging of OD predictions.

    The main annotations are described in a text file:
    <frame 1 info>
    <frame 2 info> 
    ...

    For each frame info:
    <frame image name> <bbox 1 info> <bbox 2 info> ...  

    For each bbox info:
    left,top,right,bot,class_id

    For example:
    frame1.jpg 10,10,50,50,0 
    frame2.jpg 14,13,51,52,0 20,25,80,88,1

Associated to it is a `classes.txt` (path sibling) which is a list of classes whose index correspond to the annotations' class ids (zero indexed)

## Usage

```bash
python3 -m cocojson.run.log2coco -h
```

```
usage: log2coco.py [-h] [--outjson OUTJSON] log_annot root

positional arguments:
  log_annot          Path to log annotation file
  root               Path to images root directory

optional arguments:
  -h, --help         show this help message and exit
  --outjson OUTJSON  Path to output json. Defaults to "<task_name>.json"
                     sibling to given root directory.
```
