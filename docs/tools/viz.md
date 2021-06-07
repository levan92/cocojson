# Visualise

Visualise annotations onto images. Best used for sanity check. 

Category id is written on the bounding box. Also, track id (t*), occlusion flag (oc) and iscrowd flag (cr) will be written if applicable/true  

Options:
- Write out to directory (through `--outdir`)
  - if simply flagged, will write to `viz` directory sibling to json file
  - if directory path given, will write to that given directory
- Show instantly (imshow, through `--show`) 
- Sampling (through `--sample`)

```bash
python3 -m cocojson.run.viz -h
```

## Usage

```
usage: viz.py [-h] [--outdir [OUTDIR]] [--sample SAMPLE] [--show] json imgroot

positional arguments:
  json               Path to coco json
  imgroot            Path to img root

optional arguments:
  -h, --help         show this help message and exit
  --outdir [OUTDIR]  Path to output dir, leave out to not write out
  --sample SAMPLE    Num of imgs to sample, leave this flag out to process
                     all.
  --show             To imshow
```

## Examples

```bash
python3 -m cocojson.run.viz test_datasets/merged/merged.json test_datasets/merged/images/ --sample 3 --outdir test_datasets/merged/viz --show
```

```bash
python3 -m cocojson.run.viz test_datasets/merged/merged.json test_datasets/merged/images/  --outdir
```
