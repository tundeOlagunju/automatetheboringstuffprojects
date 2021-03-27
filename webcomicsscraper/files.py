import json 
import jsonpickle
import os

def read_json_file(json_file_path):
    with open(json_file_path) as json_file:
        json_data = json.load(json_file)
        json_file.close()
        return json_data

"""
Saves to json file in pretty format
"""
def save_json(json_file_path, json_string):
    json_dict = json.loads(json_string)
    json_dumps_string = json.dumps(json_dict, indent=4)
    fout = open(json_file_path, 'w')
    print (json_dumps_string, file=fout)
    fout.close()

def save_image_to_file(content, img_file_path):
    with open(img_file_path, 'wb') as f:
        f.write(content)

def make_dir(dir):
    os.makedirs(dir, exist_ok=True)

def join_path(path_a, path_b):
    return os.path.join(path_a, path_b)

def get_base_name(url):
    # last part of the image url
    return os.path.basename(url)


        
        



