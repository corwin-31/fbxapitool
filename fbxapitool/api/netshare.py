class Netshare:
    '''
    API to confifure network sharing
    '''

    def __init__(self, access):
        self._access = access

    afp_write_parms = { 'enabled': 'bool', 'guest_allow': 'bool', 'login_name': 'text',
        'login_password': 'text', 'server_type': 'text' }
    samba_write_parms = { 'file_share_enabled': 'bool', 'logon_enabled': 'bool',
        'logon_password': 'text', 'logon_user': 'text', 'print_share_enabled': 'bool',
        'workgroup': 'text' }
    server_type = [ 'powerbook', 'powermac', 'macmini', 'imac', 'macbook', 'macbookpro',
        'macbookair', 'macpro', 'appletv', 'airport', 'xserve' ]
    afp_configuration_schema = { 'enabled': False, 'guest_allow': False, 'login_name': '',
        'login_password': '', 'server_type': server_type[0] }
    samba_configuration_schema = { 'file_share_enabled': False, 'logon_enabled': False,
        'logon_password': '', 'logon_user': '', 'print_share_enabled': True, 
        'workgroup': 'WORKGROUP' }

    def get_afp_configuration(self):
        '''
        Gets afp configuration
        '''
        return self._access.get('netshare/afp/')

    def get_samba_configuration(self):
        '''
        Gets samba configuration
        '''
        return self._access.get('netshare/samba/')

    def set_afp_configuration(self, afp_configuration):
        '''
        Sets afp configuration
        '''
        return self._access.put('netshare/afp/', afp_configuration)

    def set_samba_configuration(self, samba_configuration):
        '''
        Sets samba configuration
        '''
        return self._access.put('netshare/samba/', samba_configuration)
