class Dhcp:
    '''
    API to manage DHCP services
    '''

    def __init__(self, access):
        self._access = access

    lease_write_parms = { 'ip': 'text', 'mac': 'text', 'comment': 'text' }
    static_lease_schema = { 'ip': '', 'mac': '', 'comment': '' }
    dhcp_write_parms = {
        'always_broadcast': 'bool',
        'dns': 'list',
        'enabled': 'bool',
        'ip_range_start': 'text',
        'ip_range_end': 'text',
        'sticky_assign': 'bool'
    }
    dhcp_configuration_schema = {
        'always_broadcast': False,
        'dns': ['192.168.0.254'],
        'enabled': True,
        'ip_range_start': '192.168.0.10',
        'ip_range_end': '192.168.0.60',
        'sticky_assign': True
    }
    dhcpv6_write_parms = { 'dns': 'list', 'enabled': 'bool', 'use_custom_dns': 'bool' }
    dhcp_v6_configuration_data_schema = { 'dns': [''], 'enabled': False, 'use_custom_dns': False }


    def get_config(self):
        '''
        Gets DHCP configuration
        '''
        return self._access.get('dhcp/config/')

    def set_config(self, conf):
        '''
        Updates a config with new conf dictionary
        '''
        return self._access.put('dhcp/config/', conf)

    def get_dynamic_dhcp_lease(self):
        '''
        Gets the list of DHCP dynamic leases
        '''
        return self._access.get('dhcp/dynamic_lease/')

    def get_static_dhcp_lease(self):
        '''
        Gets the list of DHCP static leases
        '''
        return self._access.get('dhcp/static_lease/')

    def add_static_dhcp_lease(self, data):
        '''
        Adds a DHCP static lease
        '''
        return self._access.post('dhcp/static_lease/', payload=data)

    def del_static_dhcp_lease(self, id):
        '''
        Deletes a DHCP static lease with this id
        '''
        return self._access.delete('dhcp/static_lease/{0}'.format(id))

    def update_static_dhcp_lease(self, id, data):
        '''
        Updates a DHCP static lease
        '''
        return self._access.put('dhcp/static_lease/{0}'.format(id), payload=data)

    def get_v6_config(self):
        '''
        Gets DHCP v6 configuration
        '''
        return self._access.get('dhcpv6/config/')

    def set_v6_config(self, data):
        '''
        Updates DHCP v6 configuration
        '''
        return self._access.put('dhcpv6/config/', payload=data)
