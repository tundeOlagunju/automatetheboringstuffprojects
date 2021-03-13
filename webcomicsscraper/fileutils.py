# FileUtils
# class reads json files
# decodes and encodes json file
# saves it to an appropriate folder
import json
import jsonpickle

class FileUtils(object):

    @classmethod
    def read_json_file(cls, json_file_path):
        with open(json_file_path) as json_file:
            json_data = json.load(json_file)
            json_file.close()
            return json_data
    
    @classmethod
    def prepare_json_for_decoding(cls, json_input):
        for input in json_input:
            input['py/object'] = 'webcomic.WebComicDownloaddata'
        return json.dumps(json_input)
           
    @classmethod
    def decode_json(cls, json):
        prepared_json = cls.prepare_json_for_decoding(json)
        return jsonpickle.decode(prepared_json)

        
        



