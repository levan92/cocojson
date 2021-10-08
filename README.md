# cocojson

Utility functions for COCO json annotation format. The COCO Format is defined [here](./docs/coco.md).

## Install

- `cocojson` is available on pypi through `pip3 install cocojson`
- or if you prefer, clone this repo and it can be installed through `pip3 install -e .` (editable install) or `pip3 install .` as well.

## Usage

Please click into each for more details (if applicable). Links works only if you're viewing from the [github homepage](https://github.com/levan92/cocojson).


### Utility Tools

#### [Merge](./docs/tools/merge.md)

Merges multiple datasets

```bash
python3 -m cocojson.run.merge -h
```

#### [Merge from file](./docs/tools/merge_from_file.md)

Merges multiple datasets

```bash
python3 -m cocojson.run.merge_from_file -h
```

#### [Sample](./docs/tools/sample.md)

Samples k images from a dataset

```bash
python3 -m cocojson.run.sample -h
```

#### [Sample by Category](./docs/tools/sample_by_class.md)

Samples images from each category for given sample number(s).

```bash
python3 -m cocojson.run.sample_by_class -h
```

#### [Split](./docs/tools/split.md)

Split up a COCO JSON file by images into N sets defined by ratio of total images

```bash
python3 -m cocojson.run.split -h
```

#### [Visualise](./docs/tools/viz.md)

Visualise annotations onto images. Best used for sanity check.

```bash
python3 -m cocojson.run.viz -h
```

#### [Map Categories](./docs/tools/map_cat.md)

Mapping categories to a new dataset. Usually used for converting annotation labels to actual class label for training.

```bash
python3 -m cocojson.run.map_cat -h
```

#### [Filter Categories](./docs/tools/filter_cat.md)

Filter categories from COCO JSON.

```bash
python3 -m cocojson.run.filter_cat -h
```

#### [Prune Ignores](./docs/tools/ignore_prune.md)

Remove images annotated with certain "ignore" category labels. This is usually used for removing rubbish images that are pointed out by annotators to ignore frame.

```bash
python3 -m cocojson.run.ignore_prune -h
```

#### [Insert Images Meta-Information](./docs/tools/insert_img_meta.md)

Insert any extra attributes/image meta information associated with the images into the coco json file.  

```bash
python3 -m cocojson.run.insert_img_meta -h
```

#### [Split by Image Meta-Information](./docs/tools/split_by_meta.md)

Split up a COCO JSON file by images' meta-information/attributes

```bash
python3 -m cocojson.run.split_by_meta -h
```

#### [Match Images between 2 COCO JSONs](./docs/tools/match_imgs.md)

Match images between a reference COCO JSON A and COCO JSON B (to be trimmed). Any images in JSON B that is not found in JSON A will be removed (along with associated annotations)

```bash
python3 -m cocojson.run.match_imgs -h
```

#### [Extract only Annotations](./docs/tools/pred_only.md)

Get annotations/predictions only from a COCO JSON. Usually used to generate a list of predictions for COCO evaluation.

```bash
python3 -m cocojson.run.pred_only -h
```

### Converters

#### [CVAT Video XML to COCO JSON](./docs/converters/cvatvid2coco.md)

Convert CVAT Video XML to COCO JSON whilst preserving track information.

```bash
python3 -m cocojson.run.cvatvid2coco -h
```

#### CVAT Image XML to COCO JSON

_TODO_

#### [CrowdHuman odgt to COCO JSON](./docs/converters/crowdhuman2coco.md)

Converts CrowdHuman's odgt annotation format to COCO JSON format.

```bash
python3 -m cocojson.run.crowdhuman2coco -h
```

#### [Custom Object Detection Logging format to COCO JSON](./docs/converters/log2coco.md)

Converts Custom Object Detection Logging format to COCO JSON format.

```bash
python3 -m cocojson.run.log2coco -h
```

#### COCO to Darknet

_TODO_

### COCO Eval

Please use https://github.com/levan92/cocoapi.
