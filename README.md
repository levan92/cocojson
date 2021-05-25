# cocojson

Utility scripts for COCO json annotation format. The COCO Format is defined [here](./docs/coco.md).

## Install

`cocojson` package can be installed through `pip3 install -e .` (editable install) or `pip3 install .`

## Usage

### COCO Eval

Please use https://github.com/levan92/cocoapi. 

### Utility Tools

#### [Merge](./docs/merge.md)

```bash
python3 -m cocojson.run.merge -h
```

#### [Sample](./docs/sample.md)

```bash
python3 -m cocojson.run.sample -h
```

#### [Visualise](./docs/viz.md)

```bash
python3 -m cocojson.run.viz -h
```

### Converters

#### CVAT XML to COCO

##### [CVAT Video XML](./docs/cvatvid2coco.md)

```bash
python3 -m cocojson.run.cvatvid2coco -h
```

##### CVAT Image XML

_TODO_

#### COCO to Darknet

_TODO_
