import xmltodict
import click
import pandas as pd


@click.command()
@click.argument('saml_file')
def run(saml_file):
    with open(saml_file) as file:
        doc = xmltodict.parse(file.read())
    print('File successfully loaded....\n')

    errors = False
    error_list = []
    important_values = {}
    try:
        saml_attribute_assertions = {}
        for each in doc['samlp:Response']['saml:Assertion']['saml:AttributeStatement']['saml:Attribute']:
            saml_attribute_assertions[each['@Name']] = each['saml:AttributeValue']['#text']

        important_values['saml_attributes_released with corresponding values (not including name_id (please see name_id value below))'] = str(saml_attribute_assertions)
    except:
        important_values['attributes_released'] = "None or empty values present"
        error_list.append('Empty or non present attributes')
        errors = True

    important_values['name_id (ensure this value represents the correct login format from admin console)'] = doc['samlp:Response']['saml:Assertion']['saml:Subject']['saml:NameID']['#text']
    important_values['name_id_format'] = doc['samlp:Response']['saml:Assertion']['saml:Subject']['saml:NameID']['@Format']

    #ACS Url aka Reply URL, Location value from adobe metadata
    important_values['destination (must match Location attribute value from Adobe Metadata)'] = doc['samlp:Response']['@Destination']

    # Issuer URL, Entity ID from adobe metadata
    important_values['issuer_url (must match Entity ID attribute value from Adobe Metadata)'] = doc['samlp:Response']['saml:Assertion']['saml:Conditions']['saml:AudienceRestriction']['saml:Audience']

    important_values['signature_method_algorithm (should be rsa-sha1)'] = doc['samlp:Response']['ds:Signature']['ds:SignedInfo']['ds:SignatureMethod']['@Algorithm']
    important_values['digest_method_algorithm (should be rsa-sha1)'] = doc['samlp:Response']['ds:Signature']['ds:SignedInfo']['ds:Reference']['ds:DigestMethod']['@Algorithm']



    not_before = pd.to_datetime(doc['samlp:Response']['saml:Assertion']['saml:Conditions']['@NotBefore'])
    important_values['not_before'] = str(not_before)
    time_sent = pd.to_datetime(doc['samlp:Response']['@IssueInstant'])
    important_values['time_sent'] = str(time_sent)
    not_after = pd.to_datetime(doc['samlp:Response']['saml:Assertion']['saml:Conditions']['@NotOnOrAfter'])
    important_values['not_on_or_after'] = str(not_after)


    try:
        important_values['signing_cert'] = doc['samlp:Response']['ds:Signature']['ds:KeyInfo']['ds:X509Data']['ds:X509Certificate']
    except:
        error_list.append('Check presence and/or format of signing cert')
        errors = True

    file.close()

    attribute_labels = set(saml_attribute_assertions.keys())

    if time_sent >= not_after or time_sent < not_before:
        error_list.append('Time Skew Issue Found')
        errors = True

    if not {'FirstName', 'LastName', 'Email'}.issubset(attribute_labels):
        error_list.append("Issues with Attribute Labeling, check for presence and proper formatting for values: FirstName, LastName, and Email\n"
                          " Current attributes being sent: " + str(attribute_labels))
        errors = True

    print('********************************')
    print('SAML Trace Report, any errors will be printed below')
    print('******************************** \n')

    for each in important_values:
        print(each.upper() + ": ")
        print(important_values.get(each, '!!!Warning!!! Value is missing from SAML_TRACE, investigate further') + '\n')

    if errors:
        print('!!!! Common Errors Have Been Found !!!!\n')
        for each in error_list:
            print(each + '\n')
    else:
        print('-----No Common Errors Found-----')

if __name__ == '__main__':
    print('\n Attempting to run SAML Validator')
    print('example command line argument: python saml_validator.py example_trace.xml')
    print('filename of saml trace argument required')
    print('ensure .xml extension for saml trace file\n')
    run()
