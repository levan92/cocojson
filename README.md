# cocojson

Utility scripts for COCO json annotation format. The COCO Format is defined [here](./docs/coco.md).

## Install

`cocojson` package can be installed through `pip3 install -e .` (editable install) or `pip3 install .`

## Usage

Please click into each for more details (if applicable). 

### COCO Eval

Please use https://github.com/levan92/cocoapi. 

### Utility Tools

#### [Merge](./docs/merge.md)

Merges multiple datasets

```bash
python3 -m cocojson.run.merge -h
```

#### [Sample](./docs/sample.md)

Samples k images from a dataset

```bash
python3 -m cocojson.run.sample -h
```

#### [Visualise](./docs/viz.md)

Visualise annotations onto images. Best used for sanity check.

```bash
python3 -m cocojson.run.viz -h
```

#### [Map Categories](./docs/map_cat.md)

Mapping categories to a new dataset. Usually used for converting annotation labels to actual class label for training.

```bash
python3 -m cocojson.run.map_cat -h
```

#### [Prune Ignores](./docs/ignore_prune.md)

Remove images annotated with certain "ignore" category labels. This is usually used for removing rubbish images that are pointed out by annotators to ignore frame.

```bash
python3 -m cocojson.run.ignore_prune -h
```

#### [Insert Images Meta-Information](./docs/insert_img_meta.md)

Insert any extra attributes/image meta information associated with the images into the coco json file.  

```bash
python3 -m cocojson.run.ignore_prune -h
```

### Converters

#### [CVAT Video XML to COCO](./docs/cvatvid2coco.md)

Convert CVAT Video XML to COCO JSON whilst preserving track information.

```bash
python3 -m cocojson.run.cvatvid2coco -h
```

#### CVAT Image XML to COCO

_TODO_

#### [CrowdHuman odgt to COCO JSON](./docs/crowdhuman2coco.md)

Converts CrowdHuman's odgt annotation format to COCO JSON format.

```bash
python3 -m cocojson.run.crowdhuman2coco -h
```

#### COCO to Darknet

_TODO_
