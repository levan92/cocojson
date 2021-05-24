# Sample

Samples k images from a dataset

Expected format of 1 x Dataset:
    - 1 x json file 
    - 1 x Image Folder (to get to the image, path is assumed to be "Image Folder"/"file_name" given in json)


```python
python3 -m cocojson.sample_coco -h
```

```
usage: sample_coco.py [-h] [--k K] json imgroot outdir

positional arguments:
  json        Path to coco json
  imgroot     Path to img root
  outdir      Path to output dir

optional arguments:
  -h, --help  show this help message and exit
  --k K       Random k images to extract
```
