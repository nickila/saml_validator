import os
from os.path import dirname, realpath

resource_dir = dirname(realpath(__file__))

def get_resource(name):
    return os.path.join(resource_dir, name)