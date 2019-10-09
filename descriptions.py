class Descriptions:
    @classmethod
    def get_descriptions(cls):
        descriptions = {}
        descriptions['issuer_url'] = 'Must match Entity ID attribute value from Adobe Metadata'
        descriptions['destination'] = 'Must match Location attribute value from Adobe Metadata'
        descriptions['signature_method_algorithm'] = 'Should be rsa-sha1'
        descriptions['digest_method_algorithm'] = 'Should be rsa-sha1'
        return descriptions
