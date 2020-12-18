class Airmedia:
    '''
    API to manage Airmedia, partially implemented : missing receivers interaction calls
    '''

    def __init__(self, access):
        self._access = access
    
    airmedia_write_parms = { 'enabled': 'bool', 'password': 'text' }
    airmedia_configuration_schema = { 'enabled': False, 'password': '' }

    def get_config(self):
        '''
        Gets Airmedia configuration
        '''
        return self._access.get('airmedia/config/')

    def set_config(self, conf):
        '''
        Updates Airmedia configuration with conf dictionary
        '''
        return self._access.put('airmedia/config/', conf)

    def get_receivers(self):
        '''
        Gets Airmedia receivers
        '''
        return self._access.get('airmedia/receivers/')
