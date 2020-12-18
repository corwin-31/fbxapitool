class Upnpav:
    '''
    API for UPnP AV
    '''

    def __init__(self, access):
        self._access = access
    
    upnpav_write_parms = { 'enabled': 'bool' }
    upnpnav_configuration_schema = { 'enabled': False }

    def get_configuration(self):
        '''
        Gets upnpav configuration
        '''
        return self._access.get('upnpav/config/')

    def set_configuration(self, configuration):
        '''
        Sets upnpav configuration
        '''
        return self._access.put('upnpav/config/', configuration)
