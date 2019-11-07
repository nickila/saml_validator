import yaml
from flask import Flask
from backend_app.request_handler import RequestHandler
from backend_app import view
from backend_app.resources import get_resource

with open(get_resource('idp.yml')) as idp_file:
    RequestHandler.idp_repo = yaml.safe_load(idp_file)
with open(get_resource('descriptions.yml')) as d_file:
    RequestHandler.descriptions = yaml.safe_load(d_file)


app = Flask(__name__,
            template_folder=get_resource('templates'),
            static_folder=get_resource('static'))

app.register_blueprint(view.view)

if __name__ == '__main__':
    app.debug = True
    app.run()
