from pathlib import Path
from random import sample

from tqdm import tqdm
import cv2

from cocojson.utils.common import path, read_json, get_img2annots, get_setname, get_flatten_name
from cocojson.utils.draw import draw_annot

def viz(json, root, outdir=None, sample_k=None, show=False):
    img_root = path(root, is_dir=True)
    coco_dict = read_json(json)
    setname = get_setname(coco_dict, json)
    img2annots = get_img2annots(coco_dict['annotations'])

    if outdir is not None:
        if isinstance(outdir, str):
            outdir = Path(outdir)
        else:
            outdir = Path(json).parent / 'viz'
        outdir.mkdir(exist_ok=True, parents=True)

    if sample_k:
        assert sample_k > 0,'Sample must be a positive int'
        image_dicts = sample(coco_dict['images'], sample_k)
    else:
        image_dicts = coco_dict['images']

    for img_dict in tqdm(image_dicts):
        imgpath = img_root / img_dict['file_name']
        assert imgpath.is_file(),imgpath
        img = cv2.imread(str(imgpath))
        img_show = img.copy()
        for annot in img2annots[img_dict['id']]:
            draw_annot(img_show, annot) 
        if show:
            cv2.imshow(f'{setname}', img_show)
            cv2.waitKey(0)
        if outdir:
            uniq_name = get_flatten_name(img_dict['file_name'])
            writepath = outdir / f'{uniq_name}_viz.jpg' 
            cv2.imwrite(str(writepath), img_show)
    