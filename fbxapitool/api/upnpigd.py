class Upnpigd:
    '''
    API for UPnP IGD
    '''

    def __init__(self, access):
        self._access = access
    
    upnpigd_supported_versions = [ 1, 2 ]
    upnpigd_write_parms = { 'enabled': 'bool', 'version': 'int' }
    upnpig_configuration_schema = { 'enabled': True, 'version': upnpigd_supported_versions[0] }

    def delete_redir(self, id):
        '''
        Deletes the given upnpigd redirection
        '''
        return self._access.delete(f'upnpigd/redir/{id}')

    def get_configuration(self):
        '''
        Gets the upnpigd configuration
        '''
        return self._access.get('upnpigd/config/')

    def get_redirs(self):
        '''
        Gets the list of upnpigd redirections
        '''
        return self._access.get('upnpigd/redir/')

    def update_configuration(self, upnpigd_config):
        '''
        Updates the upnpigd configuration
        '''
        return self._access.put('upnpigd/config/', upnpigd_config)
