import json 
import jsonpickle
import os

def read_json_file(json_file_path):
    with open(json_file_path) as json_file:
        json_data = json.load(json_file)
        json_file.close()
        return json_data
    

def prepare_json_for_decoding(json_input):
    for input in json_input:
        input['py/object'] = 'webcomic.WebComicDownloaddata'
    return json.dumps(json_input)
           

def decode_json(json):
    prepared_json = prepare_json_for_decoding(json)
    return jsonpickle.decode(prepared_json)


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


        
        



