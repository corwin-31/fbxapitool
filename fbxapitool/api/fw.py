class Fw:
    '''
    API to manage DMZ : Firewall features
    '''

    def __init__(self, access):
        self._access = access

    ip_proto = [ 'tcp', 'udp' ]
    forwarding_write_parms = { 'comment': 'text', 'enabled': 'bool',
        'ip_proto': 'text', 'lan_ip': 'text', 'lan_port': 'int', 
        'src_ip': 'text', 'wan_port_end': 'int', 'wan_port_start': 'int' }
    port_forwarding_config_schema = { 'comment': '', 'enabled': False,
        'ip_proto': ip_proto[0], 'lan_ip': '', 'lan_port': 0, 
        'src_ip': '0.0.0.0', 'wan_port_end': 0, 'wan_port_start': 0 }
    incoming_write_parms = { 'enabled': 'bool', 'in_port': 'int' }
    incoming_port_configuration_data_schema = { 'enabled': True,
        'in_port': 0 }
    dmz_write_parms = { 'enabled': 'bool', 'ip': 'text' }
    dmz_configuration_schema = { 'enabled': False, 'ip': '' }

    def get_forward(self):
        '''
        Gets the list of port forwarding
        '''
        return self._access.get('fw/redir/')

    def update_forward(self, id, data):
        '''
        Updates a port forwarding
        '''
        return self._access.put('fw/redir/{0}'.format(id), payload=data)

    def add_forward(self, data):
        '''
        Adds a port forwarding
        '''
        return self._access.post('fw/redir/', payload=data)

    def delete_forward(self, id):
        '''
        Deletes a port forwarding
        '''
        return self._access.delete('fw/redir/{0}'.format(id))

    def get_dmz_config(self):
        '''
        Gets the dmz configuration
        '''
        return self._access.get('fw/dmz/')

    def set_dmz_config(self, conf=None):
        '''
        Sets the dmz configuration
        '''
        if conf is None:
            conf = self.dmz_configuration_schema
        return self._access.put('fw/dmz/',conf)

    def get_incoming_ports_configuration(self):
        '''
        Gets incoming ports configuration
        '''
        return self._access.get('fw/incoming/')

    def set_incoming_port(self, id, incoming_port_configuration_data):
        '''
        Sets incoming port configuration
        '''
        return self._access.put(f'fw/incoming/{id}', incoming_port_configuration_data)
