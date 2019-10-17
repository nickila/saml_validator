import xmltodict
from backend_app.process_error import ErrorHandler
#from backend_app import get_descriptions, get_idp_repo
from backend_app.analyzer import Analyzer


class RequestHandler:
    @classmethod
    def process_request(cls, request):
        try:
            saml_file = request.files['saml_file)']
            saml_dict = xmltodict.parse(request.files['saml_file'].read().decode())
        except AssertionError as e:
            ErrorHandler.process_error(e)
        idp_name = request.values['idp_name']
        idp_info = get_idp_repo().get(idp_name, None)
        return Analyzer.process(saml_dict, get_descriptions(), idp_info)
