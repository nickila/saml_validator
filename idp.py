class IDP:
    def __init__(self, name):
        idp_info = self.get_idp_info(name)
        self.name = idp_info.get('name')
        self.error_codes = idp_info.get('error_codes')
        self.helpx = idp_info.get('helpx')

    # Any new IDP documentation needs to be added here
    def get_idp_info(self, name):
        if name == 'adfs':
            adfs = {}
            adfs_help_link = 'https://helpx.adobe.com/enterprise/kb/configure-microsoft-ad-fs-with-sso.html'
            adfs['name'] = 'adfs'
            adfs['error_codes'] = {}
            adfs['helpx'] = adfs_help_link
            adfs['error_codes']['attribute_assertion'] = {'hint': 'please review steps 8 - 14',
                                                          'link': adfs_help_link + '#ConfiguretheADFSserver'}
            adfs['error_codes']['name_id'] = {'hint': 'please review step 11',
                                              'link': adfs_help_link + '#ConfiguretheADFSserver'}
            adfs['error_codes']['name_id_format'] = {'hint': 'please review step 11',
                                                     'link': adfs_help_link + '#ConfiguretheADFSserver'}
            adfs['error_codes']['issuer_url'] = {'hint': 'please review step 2',
                                                 'link': adfs_help_link + '#ConfiguretheADFSserver'}
            adfs['error_codes']['destination'] = {'hint': 'please review step 2',
                                                  'link': adfs_help_link + '#ConfiguretheADFSserver'}
            adfs['error_codes']['signature_method'] = {'hint': 'please review step 16',
                                                       'link': adfs_help_link + '#ConfiguretheADFSserver'}
            adfs['error_codes']['digest_method'] = {'hint': 'please review step 16',
                                                    'link': adfs_help_link + '#ConfiguretheADFSserver'}
            return adfs
        elif name == 'shibboleth':
            shib = {}
            shib_help_link = 'https://helpx.adobe.com/enterprise/kb/configure-shibboleth-with-adobe-sso.html'
            shib['name'] = 'shibboleth'
            shib['error_codes'] = {}
            shib['helpx'] = shib_help_link
            shib['error_codes']['attribute_assertion'] = {'hint1': 'please review step 2',
                                                          'link1': shib_help_link + '#ConfigureShibboleth',
                                                          'hint2': 'please review step 1',
                                                          'link2': shib_help_link + '#TroubleshootyourShibbolethsetup'}
            shib['error_codes']['name_id'] = {'hint': 'please review step 1 and 3',
                                              'link': shib_help_link + '#TroubleshootyourShibbolethsetup'}
            shib['error_codes']['name_id_format'] = {'hint1': 'please review step 2',
                                                     'link1': shib_help_link + '#TroubleshootyourShibbolethsetup',
                                                     'hint2': 'please review step 8',
                                                     'link2': shib_help_link + '#configuration'}
            shib['error_codes']['issuer'] = {'hint': 'please review step 3',
                                             'link': shib_help_link + '#ConfigureShibboleth'}
            shib['error_codes']['destination'] = {'hint': 'please review step 3',
                                                  'link': shib_help_link + '#ConfigureShibboleth'}

            return shib

    # def retrieve_data(self):
    #     database = deepcopy(self.database)
    #     info = deepcopy(database.get(self.name))
    #     return info
    #
    # # ALL new IDP documentation must be added to here
    # def fill_database(self):
    #     self.database.update({'adfs':
    #                               {'error_codes':
    #                                    {'attribute_labels':
    #                                         {'description': '', 'links': []}},
    #                                # {'name_id_format': ''},
    #                                'help_link': 'https://helpx.adobe.com/enterprise/kb/configure-microsoft-ad-fs-with-sso.html'}})
    #     self.database.update({'shibboleth':
    #                               {'error_codes':
    #                                    {'attribute_labeling':
    #                                         {'description': '', 'links': []}},
    #                                'help_link': 'https://helpx.adobe.com/enterprise/kb/configure-shibboleth-with-adobe-sso.html'}})
    #     self.database.update({'azure':
    #                               {'error_codes':
    #                                    {'attribute_labeling':
    #                                         {'description': '', 'links': []}},
    #                                'help_link': 'https://helpx.adobe.com/enterprise/kb/configure-microsoft-azure-with-adobe-sso.html'}})
    #     self.database.update({'okta':
    #                               {'error_codes':
    #                                    {'attribute_labeling':
    #                                         {'description': '', 'links': []}},
    #                                'help_link': 'https://helpx.adobe.com/enterprise/kb/configure-okta-with-adobe-sso.html'}})
    #     self.database.update({'wso2':
    #                               {'error_codes':
    #                                    {'attribute_labeling':
    #                                         {'description': '', 'links': []}},
    #                                'help_link': 'https://helpx.adobe.com/enterprise/kb/configure-wso2-idp-adobe-sso.html'}})
    #     self.database.update({'google':
    #                               {'error_codes':
    #                                    {'attribute_labeling':
    #                                         {'description': '', 'links': []}},
    #                                'help_link': 'https://helpx.adobe.com/enterprise/kb/configure-google-with-adobe-sso.html'}})
