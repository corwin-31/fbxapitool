class Connection:
    '''
    API to manage Internet connection
    '''

    def __init__(self, access):
        self._access = access
    
    configuration_write_parms = { 'ping': 'bool',
        'remote_access': 'bool', 'remote_access_port': 'int',
        'allow_token_request': 'bool', 'adblock': 'bool',
        'remote_access': 'bool', 'wol': 'bool', 'https_port': 'int',
        'https_available': 'bool', 'disable_guest': 'bool' }
    configuration_data_schema = { 'ping': False, 'remote_access': False,
        'remote_access_port': 32767, 'allow_token_request': True,
        'adblock': True, 'remote_access': False, 'wol': True,
        'https_port': 32769, 'https_available': True, 
        'disable_guest': True }
    ipv6_write_parms = { 'ipv6_enabled': 'bool', 'ipv6_firewall': 'bool',
        'delegations': 'list-multi' }
    ipv6_data_schema = { 'ipv6_enabled': True, 'ipv6_firewall': True,
        'delegations': [] }
    ddns_write_parms = { 'enabled': 'bool', 'hostname': 'text',
    'user': 'text', 'password': 'text' }
    ddns_data_schema = { 'enabled': False, 'hostname': '', 'user': '',
        'password': '' }
    ddns_providers = [ 'dyndns', 'ovh', 'noip' ]
    lte_configuration_data_schema = { 'enabled': True }

    def get_status(self):
        '''
        Gets Connection status
        '''
        return self._access.get('connection')

    def get_config(self):
        '''
        Gets the current Connection configuration
        '''
        return self._access.get('connection/config')

    def set_config(self, conf):
        '''
        Updates the Connection configuration
        '''
        return self._access.put('connection/config', conf)

    def get_ipv6_config(self):
        '''
        Gets the current IPv6 Connection configuration
        '''
        return self._access.get('connection/ipv6/config')

    def set_ipv6_config(self, conf):
        '''
        Updates the IPv6 Connection configuration
        '''
        return self._access.put('connection/ipv6/config', conf)

    def get_xdsl_stats(self):
        '''
        Gets port_id xDSL stats
        '''
        return self._access.get('connection/xdsl')

    def get_ftth_stats(self):
        '''
        Gets the current FTTH status
        '''
        return self._access.get('connection/ftth')

    def get_dyndns_status(self, provider=ddns_providers[0]):
        '''
        Gets status of the DynDNS service for a provider
        Usually provider can be dyndns (default), ovh or noip
        '''
        return self._access.get(f"connection/ddns/{provider}/status/")

    def get_dyndns_config(self, provider=ddns_providers[0]):
        '''
        Gets configuration of the DynDNS service for a provider
        Usually provider can be dyndns (default), ovh or noip
        '''
        return self._access.get(f"connection/ddns/{provider}/")

    def set_dyndns_config(self, conf, provider=ddns_providers[0]):
        '''
        Sets configuration of the DynDNS service for a provider
        Usually provider can be dyndns (default), ovh or noip
        '''
        return self._access.put(f"connection/ddns/{provider}/", conf)

    def get_status_details(self):
        '''
        Gets Connection detailed status
        '''
        return self._access.get('connection/full')

    def get_logs(self):
        '''
        Gets Connection logs
        '''
        return self._access.get('connection/logs')

    def remove_connection_logs(self):
        '''
        Removes connection logs
        '''
        return self._access.delete('connection/logs/')

    def get_lte_config(self):
        '''
        Gets lte connection configuration
        '''
        return self._access.get('connection/lte/config/')

    def set_lte_config(self, lte_configuration_data=lte_configuration_data_schema):
        '''
        Updates lte connection configuration
        '''
        return self._access.put('connection/lte/config/', lte_configuration_data)
