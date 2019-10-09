from flask import Flask, render_template, request, jsonify
import xmltodict
from saml_validation import parse_saml, analyze
from idp import IDP

app = Flask(__name__, instance_relative_config=True)

# from werkzeug.debug import DebuggedApplication
# appx = DebuggedApplication(app, evalex=True)

@app.route('/')
def welcome():
    return render_template('front.html')


@app.route('/upload', methods=['POST'])
def upload():
    idp_name = request.values['idp_name']
    saml_dict = xmltodict.parse(request.files['saml_file'].read().decode())
    saml_values = parse_saml(saml_dict)
    idp_info = IDP.get_idp_info(idp_name) if idp_name != 'other' else None
    result = analyze(saml_values, idp_info)

    return jsonify(result.result)


if __name__ == '__main__':
    app.debug = True
    app.run()
