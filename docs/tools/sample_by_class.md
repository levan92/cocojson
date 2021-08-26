# Sample by class

Samples images from each category for given sample number(s).

You can give either an integer or a list of integer to set the number of images to sample for each category (if single int given, it will apply to all categories).

If max_img is given, an upper limit will be impose on the total number of images of the sampled dataset. It will keep retrying the sampling until it falls under this upper limit, or it will raise an exception if it retries too many times without succeeding.

Expected format of 1 x Dataset:
- 1 x json file 
- 1 x Image Folder (to get to the image, path is assumed to be "Image Folder"/"file_name" given in json)

Will output new dataset in given `outdir`, with new json file (same name as original json name) and `images` directory.

## Usage

```bash
python3 -m cocojson.sample_by_class -h
```

```
usage: sample_by_class.py [-h] [--class-ks [CLASS_KS [CLASS_KS ...]]]
                          [--max-img MAX_IMG] [--retries RETRIES]
                          json imgroot outdir

positional arguments:
  json                  Path to coco json
  imgroot               Path to img root
  outdir                Path to output dir

optional arguments:
  -h, --help            show this help message and exit
  --class-ks [CLASS_KS [CLASS_KS ...]]
                        How many to sample for each category, can either be
                        single int or a list of int corresponding to each
                        category. Defaults to 10 per category.
  --max-img MAX_IMG     Max num of images to be sampled, will retry until it
                        falls below. Defaults to no max limit.
  --retries RETRIES     Max number of retries. Defaults to 1000.
  ```

## Examples

```bash
python3 -m cocojson.run.sample_by_class /data/cute_kittens_puppies/catdog.json /data/cute_kittens_puppies/catdog /data/cute_kittens_puppies/smaller_set --class-ks 10
```

```bash
python3 -m cocojson.run.sample_by_class /data/cute_kittens_puppies/catdog.json /data/cute_kittens_puppies/catdog /data/cute_kittens_puppies/smaller_set --class-ks 1 1 1 1 3 --max-img 3 --retries 10
```
