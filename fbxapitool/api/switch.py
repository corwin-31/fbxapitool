class Switch:
    '''
    API to manage the switch
    '''

    def __init__(self, access):
        self._access = access

    switch_duplex = [ 'auto', 'full', 'half' ]
    switch_speed = [ 'auto', '10', '100', '1000' ]
    switch_port_write_parms = { 'duplex': 'text', 'speed': 'text' }
    switch_port_configuration_schema = { 'duplex': switch_duplex[0], 'speed': switch_speed[0] }

    def get_status(self):
        '''
        Gets Switch status
        '''
        return self._access.get('switch/status/')

    def get_port_conf(self, port_id):
        '''
        Gets port #port_id configuration
        '''
        return self._access.get('switch/port/{0}'.format(port_id))

    def set_port_conf(self, port_id, conf=switch_port_configuration_schema):
        '''
        Updates port #port_id configuration
        '''
        return self._access.put('switch/port/{0}'.format(port_id), conf)

    def get_port_stats(self, port_id):
        '''
        Gets port #port_id stats
        '''
        return self._access.get('switch/port/{0}/{1}'.format(port_id, 'stats'))
