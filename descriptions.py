class Descriptions:
    @classmethod
    def get_descriptions(cls):
        descriptions = {}
        descriptions['issuer_url'] = 'Must match Entity ID attribute value from Adobe Metadata'
        descriptions['destination'] = 'Must match Location attribute value from Adobe Metadata'
        descriptions['signature_method_algorithm'] = 'Should be rsa-sha1'
        descriptions['digest_method_algorithm'] = 'Should be rsa-sha1'
        descriptions['assertion_attributes'] = 'Attributes included in your SAML assertion'
        descriptions['name_id_format'] = 'Format of your Name-ID attribute'
        descriptions['name_id'] = 'Name-ID attribute,' \
                                  ' format of attribute must match your login setting of your federated directory'
        descriptions['signing_cert'] = 'Token-Signing Certificate, must be Base-64 encoded X.509(.CER),' \
                                       ' which is equivalent to a PEM format certificate'
        descriptions['time_sent'] = "Timestamp must be within the 'not_before' and 'not_on_or_after' time window"
        return descriptions
