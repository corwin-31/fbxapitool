class Ftp:
    '''
    API for configuring FTP
    '''

    def __init__(self, access):
        self._access = access

    ftp_write_parms = { 'enabled': 'bool', 'allow_anonymous': 'bool', 'allow_anonymous_write': 'bool',
        'allow_remote_access': 'bool', 'remote_domain': 'text', 'password': 'text',
        'port_ctrl': 'int', 'port_data': 'int' }
    ftp_configuration_schema = { 'enabled': False, 'allow_anonymous': False, 'allow_anonymous_write': False,
        'allow_remote_access': False, 'remote_domain': '', 'password': '',
        'port_ctrl': 12345, 'port_data': 45678 }

    def get_ftp_configuration(self):
        '''
        Gets ftp configuration
        '''
        return self._access.get('ftp/config/')

    def set_ftp_configuration(self, ftp_configuration):
        '''
        Sets ftp configuration
        '''
        return self._access.put('ftp/config/', ftp_configuration)
