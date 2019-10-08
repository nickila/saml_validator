class IDP:
    # Any new IDP documentation needs to be added here
    @classmethod
    def get_idp_info(self, name):
        if name == 'adfs':
            adfs = {}
            adfs_help_link = 'https://helpx.adobe.com/enterprise/kb/configure-microsoft-ad-fs-with-sso.html'
            adfs['name'] = 'adfs'
            adfs['error_codes'] = {}
            adfs['helpx'] = adfs_help_link
            adfs['error_codes']['assertion_attributes'] = {'hint': 'please review steps 8 - 14',
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
            shib['error_codes']['assertion_attributes'] = {'hint1': 'please review step 2',
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
