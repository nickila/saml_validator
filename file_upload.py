from flask import Flask, render_template, request, jsonify
import xmltodict
from web_saml_validator import saml_analysis

app = Flask(__name__, instance_relative_config=True)


@app.route('/')
def welcome():
    return render_template('front.html')


@app.route('/upload', methods=['POST'])
def upload():
    analysis = saml_analysis(xmltodict.parse(request.files['saml_file'].read().decode()))

    return jsonify(analysis)


if __name__ == '__main__':
    app.debug = True
    app.run()
