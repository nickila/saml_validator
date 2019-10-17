import os
import yaml
from flask import Flask
from backend_app.resources import resource_dir
my_app = Flask(__name__,
            template_folder=os.path.join(resource_dir, 'templates'),
            static_folder=os.path.join(resource_dir, 'static'))
import backend_app.views

with open('configurations/idp.yml') as c_file:
    idp_repo = yaml.safe_load(c_file)
    c_file.close()
with open('configurations/descriptions.yml') as d_file:
    descriptions = yaml.safe_load(d_file)
    d_file.close()


def get_descriptions():
    return descriptions


def get_idp_repo():
    return idp_repo


if __name__ == '__main__':
    my_app.debug = True
    my_app.run()