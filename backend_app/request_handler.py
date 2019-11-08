import xmltodict
from backend_app.analyzer import Analyzer
from backend_app.error_handler import XMLParsingError, FileUploadError


class RequestHandler:
    idp_repo = None
    descriptions = None

    @classmethod
    def process_request(cls, request):
        data = cls.validate_xml_upload(request)
        saml_dict = cls.dict_parse_xml(data)
        idp_name = request.values.get('idp_name', None)
        idp_info = cls.idp_repo.get(idp_name, {})
        return Analyzer.process(saml_dict, cls.descriptions, idp_info)

    @classmethod
    def validate_xml_upload(cls, request):
        """
        description: validates that a file and been uploaded and that the files is in .xml format. Also, reads()
        and decode() the uploaded file into a string object.
        :param request: Flask request object
        :return: str() representation of the uploaded .xml file
        """
        try:
            file = request.files['saml_file']
            # x = file.read()
            # print()
        except Exception as e:
            raise FileUploadError('No file found. Please upload an xml saml trace ' + str(e))
        if 'xml' not in file.content_type and 'xml' not in file.mimetype:
            raise FileUploadError('.xml format required')
        try:
            data = file.read()
        except Exception as e:
            raise FileUploadError('Error reading and decoding XML file ' + str(e))
        try:
            return data.decode()
        except AttributeError:
            return data

    @classmethod
    def dict_parse_xml(cls, data):
        """
        description: attempts to parse the str(.xml file) into a dict() via xmltodict.parse()
        :param data: str() representation of .xml file
        :return: dict() representation of .xml file
        """
        try:
            # converting orderedDict() to dict()
            return dict(xmltodict.parse(data))
        except Exception as e:
            raise XMLParsingError('Error parsing XML: ' + str(e))
