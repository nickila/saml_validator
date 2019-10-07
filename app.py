from flask import Flask, render_template, request, jsonify
import xmltodict
from saml_validation import saml_analysis

app = Flask(__name__, instance_relative_config=True)


@app.route('/')
def welcome():
    return render_template('front.html')


@app.route('/upload', methods=['POST'])
def upload():
    idp_name = request.values['idp_name']
    saml_dict = xmltodict.parse(request.files['saml_file'].read().decode())
    analysis = saml_analysis(saml_dict, idp_name)

    return jsonify(analysis)


if __name__ == '__main__':
    app.debug = True
    app.run()
