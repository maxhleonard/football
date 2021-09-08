import pkg_resources
import json



def get_data_file(filename):

    file_path = pkg_resources.resource_filename("FootballStats", "data/{filename}".format(filename=filename))
    with open(file_path) as f:
        data = json.load(f)
        f.close()
    return data

