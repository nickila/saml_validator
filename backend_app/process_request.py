import xmltodict
from backend_app.analyzer import Analyzer


class RequestHandler:
    idp_repo = None
    descriptions = None
    @classmethod
    def process_request(cls, request):
        try:
            saml_dict = xmltodict.parse(request.files['saml_file'].read().decode())
        except Exception as e:
            raise XMLParsingError(str(e))
        idp_name = request.values['idp_name']
        idp_info = cls.idp_repo[idp_name] if idp_name != 'other' else None
        return Analyzer.process(saml_dict, cls.descriptions, idp_info)


class XMLParsingError(Exception):
    pass
