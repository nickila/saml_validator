import xmltodict
from flask import Flask, render_template, request, jsonify
import yaml
from saml_validation import parse_saml, analyze

app = Flask(__name__, instance_relative_config=True)

# from werkzeug.debug import DebuggedApplication
# appx = DebuggedApplication(app, evalex=True)
with open('configuration.yml') as file:
    idp_repo = yaml.safe_load(file)


@app.route('/')
def welcome():
    return render_template('front.html')


@app.route('/upload', methods=['POST'])
def upload():
    idp_name = request.values['idp_name']
    saml_dict = xmltodict.parse(request.files['saml_file'].read().decode())
    saml_values = parse_saml(saml_dict)
    idp_info = idp_repo.get(idp_name, None)
    result = analyze(saml_values, idp_info)

    return jsonify(result)


if __name__ == '__main__':
    app.debug = True
    app.run()
