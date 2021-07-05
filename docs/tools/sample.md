# Sample

Samples `k` images from a dataset and uses that to build a new dataset. Useful for experimentation with a "lite" dataset.

Expected format of 1 x Dataset:
- 1 x json file 
- 1 x Image Folder (to get to the image, path is assumed to be "Image Folder"/"file_name" given in json)

Will output new dataset in given `outdir`, with new json file (same name as original json name) and `images` directory. 

## Usage

```bash
python3 -m cocojson.sample -h
```

```
usage: sample.py [-h] [--k K] json imgroot outdir

positional arguments:
  json        Path to coco json
  imgroot     Path to img root
  outdir      Path to output dir

optional arguments:
  -h, --help  show this help message and exit
  --k K       Random k images to extract
```
