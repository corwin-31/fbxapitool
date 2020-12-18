class Lan:
    '''
    API for LAN management
    '''

    def __init__(self, access):
        self._access = access

    lan_mode = [ 'router', 'bridge' ]
    lanconf_write_parms = { 'ip': 'text', 'name': 'text', 'name_dns': 'text', 'name_mdns': 'text', 'mode': 'text', 'name_netbios': 'text' }
    lan_configuration_schema = { 'ip': '192.168.0.254', 'name': 'Freebox Server', 'name_dns': 'freebox-server', 'name_mdns': 'Freebox-Server', 'mode': 'router', 'name_netbios': 'Freebox_Server' }
    host_type = [ 'workstation', 'laptop', 'smartphone', 'tablet', 
        'printer', 'vg_console', 'television', 'nas', 'ip_camera',
        'ip_phone', 'freebox_player', 'freebox_hd', 'freebox_crystal',
        'freebox_mini', 'freebox_delta', 'freebox_one', 'freebox_wifi',
        'freebox_pop', 'networking_device', 'multimedia_device', 'other' ]
    lanhost_write_parms = { 'primary_name': 'text', 'host_type': 'text', 'persistent': 'bool' }
    lan_host_data_schema = { 'primary_name': '', 'host_type': host_type[0], 'persistent': False }
    wol_write_parms = { 'mac': 'text', 'password': 'text' }
    wol_schema = { 'mac': '', 'password': '' }

    def get_config(self):
        '''
        Gets Lan configuration
        '''
        return self._access.get('lan/config/')

    def set_config(self, conf):
        '''
        Updates Lan config with conf dictionary
        '''
        return self._access.put('lan/config/', conf)

    def get_interfaces(self):
        '''
        Get browsable Lan interfaces
        '''
        return self._access.get('lan/browser/interfaces')

    def get_hosts_list(self, interface='pub'):
        '''
        Get the list of hosts on a given interface¶
        '''
        return self._access.get('lan/browser/{0}'.format(interface))

    def get_host_information(self, host_id, interface='pub'):
        '''
        Gets specific host informations on a given interface¶
        '''
        return self._access.get('lan/browser/{0}/{1}'.format(interface, host_id))

    def set_host_information(self, host_id, conf, interface='pub'):
        '''
        Updates specific host informations on a given interface¶
        '''
        return self._access.put('lan/browser/{0}/{1}'.format(interface, host_id), conf)

    def wol(self, data, interface='pub'):
        '''
        Wakes up on lan a device
        '''
        return self._access.post('lan/wol/{0}/'.format(interface), data)

    def delete_lan_host(self, host_id, interface='pub'):
        '''
        Deletes lan host
        '''
        return self._access.delete(f'lan/browser/{interface}/{host_id}/')
