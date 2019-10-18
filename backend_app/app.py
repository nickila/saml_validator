import yaml
from flask import Flask

from backend_app import view
from backend_app.resources import get_resource

with open(get_resource('idp.yml')) as c_file:
    idp_repo = yaml.safe_load(c_file)
    c_file.close()
with open(get_resource('descriptions.yml')) as d_file:
    descriptions = yaml.safe_load(d_file)
    d_file.close()


def get_descriptions():
    return descriptions


def get_idp_repo():
    return idp_repo


app = Flask(__name__,
            template_folder=get_resource('templates'),
            static_folder=get_resource('static'))

app.register_blueprint(view.view)

if __name__ == '__main__':
    app.debug = True
    app.run()
