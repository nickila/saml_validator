import pytest
import xmltodict
from werkzeug.datastructures import FileStorage

from backend_app.analyzer import Analyzer
from backend_app.error_handler import SamlParsingError


# Placeholder for test on Analyzer.get_attribute_value()
def test_get_attribute_value():
    nested_dict = {'level1':
        {'level2': {
            'property': 'example',
            'level3': {'property2': 'example',
                       'final': {'key': 'value'}}
        }}}
    expected = {'key': 'value'}
    result = Analyzer.get_attribute_value(nested_dict, ['level1', 'level2', 'level3', 'final'])
    assert expected == result


def test_parse_saml(saml_file_dict, saml2_file_dict, saml_parsed_dict, saml2_parsed_dict):
    result = Analyzer.parse_saml(saml_file_dict)
    expected = saml_parsed_dict
    assert result == expected

    # testing saml2 key
    result = Analyzer.parse_saml(saml2_file_dict)
    expected = saml2_parsed_dict
    assert result == expected

    # asserts SamlParsingError exception is thrown when no saml values are found
    with pytest.raises(SamlParsingError):
        Analyzer.parse_saml({'saml3p': {}})


def test_create_error_dict(saml_parsed_dict, descriptions, idp_repo):
    # checks compatibility with all idp options
    for each in {'google', 'adfs', 'shibboleth', 'azure', 'okta', 'wso2'}:
        result = Analyzer.create_error_dict(saml_parsed_dict, descriptions.get('error_message'), idp_repo.get(each))
        assert result == {}

    result = Analyzer.create_error_dict(saml_parsed_dict, descriptions.get('error_message'))
    assert result == {}

    saml_parsed_dict['name_id_format'] = 'transient'
    saml_parsed_dict['signing_cert'] = None
    saml_parsed_dict['name_id'] = None
    saml_parsed_dict['assertion_attributes'] = None
    result = Analyzer.create_error_dict(saml_parsed_dict, descriptions.get('error_message'), idp_repo['adfs'])
    assert {'assertion_attributes', 'name_id_format', 'signing_cert'}.issubset(result)

    saml_parsed_dict['assertion_attributes'] = {'astName': 'wrong', 'FirstName': 'right', 'Email': 'right'}
    result = Analyzer.create_error_dict(saml_parsed_dict, descriptions.get('error_message'), idp_repo['adfs'])
    assert 'assertion_attributes' in result


@pytest.fixture
def saml_file_dict():
    with open('fixtures/saml_trace.xml') as xml:
        file = FileStorage(content_type='application/xml', name='saml_file', stream=xml)
        data = file.read()
        return dict(xmltodict.parse(data))


@pytest.fixture
def saml2_file_dict():
    with open('fixtures/saml2_trace.xml') as xml:
        file = FileStorage(content_type='application/xml', name='saml_file', stream=xml)
        data = file.read()
        return dict(xmltodict.parse(data))
