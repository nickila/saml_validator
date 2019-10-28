import xmltodict
from backend_app.analyzer import Analyzer
from backend_app.error_handler import XMLParsingError, InternalError, NoFilePresentError, FileUploadError


class RequestHandler:
    idp_repo = None
    descriptions = None
    @classmethod
    def process_request(cls, request):
        file = cls.validate_xml_upload(request)
        saml_dict = cls.dict_parse_xml(file)
        try:
            idp_name = request.values.get('idp_name', 'Other/Not Specified')
            idp_info = cls.idp_repo[idp_name] if idp_name != 'Other/Not Specified' else None
            descriptions = cls.descriptions
        except Exception as e:
            raise InternalError(str(e))

        return Analyzer.process(saml_dict, descriptions, idp_info)

    @classmethod
    def validate_xml_upload(cls, request):
        if 'saml_file' not in request.files:
            raise NoFilePresentError(str(Exception))
        else:
            file = request.files['saml_file']
        if 'xml' not in file.content_type and 'xml' not in file.mimetype:
            raise FileUploadError(str(Exception))
        return file

    @classmethod
    def dict_parse_xml(cls, file):
        try:
            saml_dict = xmltodict.parse(file.read().decode())
        except Exception as e:
            raise XMLParsingError(str(e))
        return saml_dict
