import json
from shutil import copy
from pathlib import Path

def read_json(json_path):
    with open(json_path, 'r') as f:
        d = json.load(f)    
    return d

def write_json(json_path, dic):
    with open(json_path, 'w') as f:
        json.dump(dic, f)    

def assure_copy(src, dst):
    assert Path(src).is_file()
    Path(dst).parent.mkdir(exist_ok=True, parents=True)
    copy(src, dst)