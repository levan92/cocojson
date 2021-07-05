'''
Samples k images from a dataset. 

Expected format of 1 x Dataset:
    - 1 x json file 
    - 1 x Image Folder (to get to the image, path is assumed to be "Image Folder"/"file_name" given in json)

Will output new dataset in given `outdir`, with new json file (same name as original json name) and `images` directory. 
'''

from pathlib import Path
from shutil import copy
from random import sample as _sample

from cocojson.utils.common import read_json, write_json, path

def sample(json_path, imgroot, outdir, k=10):
    json_path = path(json_path)
    imgroot_path = path(imgroot, is_dir=True)

    outdir = Path(outdir)
    outroot_path = outdir / 'images'
    outroot_path.mkdir(exist_ok=True, parents=True)

    assert k > 0

    coco_dict = read_json(json_path)

    sampled = _sample(coco_dict['images'], k)

    new_imgs = []
    chosen_img_ids = []
    for img_dict in sampled:
        imgpath = imgroot_path / img_dict['file_name']
        assert imgpath.is_file()

        newip = outroot_path / img_dict['file_name']
        newip.parent.mkdir(exist_ok=True, parents=True)

        print(f'{imgpath}-->{newip}')
        copy(imgpath, newip)

        chosen_img_ids.append(img_dict['id'])
        new_imgs.append(img_dict)

    new_annots = []
    for annot in coco_dict['annotations']:
        if annot['image_id'] in chosen_img_ids:
            new_annots.append(annot)

    coco_dict['images'] = new_imgs
    coco_dict['annotations'] = new_annots

    out_json = outdir / json_path.name
    write_json(out_json, coco_dict)

